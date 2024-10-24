<template>
    <div style="height: 100vh; position:relative">
        <div
            v-if="!loading"
            class="d-flex align-center justify-center "
            style="width: 100%;
            background: #3a3a3a29;
            position: absolute;
            z-index: 100;
            height: 100%;
            "
            >
            <div>
                <v-progress-circular
                    :size="100"
                    :width="7"
                    color="blue"
                    indeterminate
                ></v-progress-circular>
            </div>
        </div>
        <div style="height: 100%; width: 100%;
        position: absolute;
        z-index:1">
            <div
                class="d-flex flex-column"
                style="height: 100%; background: #f5f5f599"
            >
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "shell-with-loading",
    props: {
        loading: {
            type: Boolean,
        },
    },
};
</script>

<style lang="scss" scoped>
</style>