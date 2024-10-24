<template>
    <div>
        <form-password :multiData="multiData" @save="save"></form-password>
    </div>
</template>

<script>
import FormPassword from '@/components/statistic/FormPassword.vue'
import { createNamespacedHelpers } from "vuex";
const { mapActions } = createNamespacedHelpers("filterslogic");

    export default {
        name: "add-password",
        components: { FormPassword },
        data() {
            return {
                multiData: {}
            }
        },
        methods: {
            ...mapActions([
                "getFiltersWithoutRecord",
            ]),
            save(data) {
                
                this.$http
                .post('/api/statistic/passport/', {data, method: "add"})
                .then((data) => {
                    if (data.data != '' && 'error' in data.data) {
                        alert(data.data.error)
                    } else {
                        alert('Паспорт создался успешно')
                    }
                    
                })
                .catch((error) => {
                    console.dir(error);
                })
            }
        },
        mounted() {
            this.getFiltersWithoutRecord({
                sub_system: [{ name: "sub_system", related_name: "name", sort: "none" }],
                priority: [{ name: "priority", related_name: "name", sort: "none" }],
                criticality: [{ name: "criticality", related_name: "name", sort: "none" }],
                responsible: [{ name: "responsible", related_name: "name", sort: "none" }],
                
            })
            .then((data) => {
                this.multiData = data;

            })
        }
        
    }
</script>

<style lang="scss" scoped>

</style>