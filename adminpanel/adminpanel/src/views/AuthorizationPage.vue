<template>
    <div>
        <div>
            <InputText id="username" v-model="value" placeholder="Логин" class="p-10"/>
        </div>
        <div class="p-40">
            <Password v-model="value" :feedback="false"  placeholder="Логин"/>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
const value = ref(null);
</script>

<style>
/* .login {
    padding: 10px;
} */
</style>
