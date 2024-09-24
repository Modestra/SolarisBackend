<template>
    <div>
        <div>
            <InputText id="username" v-model="login" placeholder="Логин"/>
        </div>
        <div class="p-40">
            <Password v-model="password" :feedback="false"  placeholder="Пароль"/>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
const login = ref(null);
const password = ref(null);
</script>

<style>
</style>
