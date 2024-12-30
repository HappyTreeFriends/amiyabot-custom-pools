<template>
    <n-config-provider class="container" :theme-overrides="themeOverrides">
        <router-view />
    </n-config-provider>
</template>

<script setup lang="ts">
import type { GlobalThemeOverrides } from 'naive-ui'

const themeOverrides: GlobalThemeOverrides = {
    common: {
        primaryColor: '#7b40f2',
        primaryColorHover: '#7b40f2',
        primaryColorPressed: '#6d24ff',
        primaryColorSuppl: '#d8c9f7'
    }
}
</script>

<style scoped lang="scss">
.container {
    width: 100%;
    height: 100%;
    font-size: 14px;
    overflow: hidden;
}
</style>