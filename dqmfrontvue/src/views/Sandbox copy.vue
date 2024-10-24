<template>
  <div id="sandbox">
    <FlowGenerator></FlowGenerator>

  </div>
</template>

<script>
import FlowGenerator from "./FlowGenerator.vue";

export default {
  name: "sandbox",
  components: {
    FlowGenerator,
  },
  data() {
    return {
      display: false,
      prop: []
    };
  },
  methods: {
    displayProperties() {
      this.display = !this.display;
    }
  },
  mounted() {
    //Receives signal from FlowGenerator.vue and displays properties
    eventBus.$on("displayProperties", propertyArray => {
      this.displayProperties();
      this.prop = propertyArray;
    });
  }
};
</script>

<style>
body {
  font-family: "Avenir", Arial, Helvetica, sans-serif;
  color: #2c3e50;
}
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

#cell {
  position: relative;
  width: 300;
  height: 800;
  border: 2px solid black;
  right: 0px;
}
</style>
