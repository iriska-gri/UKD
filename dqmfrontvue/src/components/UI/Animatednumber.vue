<template>
  <span class="tweened-number">{{ formatter(tweeningValue) }}</span>
</template>

<script>
let TWEEN = require('@tweenjs/tween.js');
export default {
  props: {
    // The value that we'll be tweening to.
    value: {
      type: Number,
      required: true,
      default: 0
    },
    fixed:{
      type:Number,
      default:0
    },

    // How long the tween should take. (In milliseconds.)
    tweenDuration: {
      type: Number,
      default: 500
    }
  },

  watch: {
    // Whenever `props.value` changes, update the tween.
    value(newVal, oldVal) {
      
      this.tween(oldVal, newVal)
    }
  },

  // This holds the temporary state of the tweened value.
  data() {
    return {
      tweeningValue: 0
    }
  },

  mounted() {
    this.tween(0, this.value)
  },

  methods: {
    // This is our main logic block. It handles tweening from a start value to an end value.
    formatter(integer){
      return ((integer>=10000)||(integer<=-10000))?new Intl.NumberFormat('ru-RU').format(integer):integer
    },
    tween(start, end) {
      let frameHandler

      // Handles updating the tween on each frame.
      const animate = function (currentTime) {
        TWEEN.update(currentTime)
        frameHandler = requestAnimationFrame(animate)
      }

      const myTween = new TWEEN.Tween({ tweeningValue: start })
      .to({ tweeningValue: end }, this.tweenDuration)
      // Be careful to not to do too much here! It will slow down the app.
      .onUpdate((myTween) => {
        this.tweeningValue = myTween.tweeningValue.toFixed(this.fixed)
      })
      .onComplete(() => {
        // Make sure to clean up after ourselves.
        cancelAnimationFrame(frameHandler)
        
      })
      // This actually starts the tween.
      .start()

      frameHandler = requestAnimationFrame(animate)
    }
  }
}
</script>