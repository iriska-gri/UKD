<template>
    <div>
        <v-text-field
            
            :style="{'fontSize': fontSize, 'width': '60px'}"
            outlined
            dense
            hide-details="false"
        > </v-text-field>
    </div>
</template>

<script>
    export default {
        name: "passport-input",
        props: {
            fontSize: {
                type: String,
                default: "1em"
            }
        }
    }
</script>

<style lang="scss" scoped>
    
</style>