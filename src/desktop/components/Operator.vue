<template>
  <div class="operator">
    <div class="operator-name">
      <span>界·徐盛</span>
      <img class="operator-class" src="/classes/WARRIOR.png" />
    </div>
    <div class="rarity">
      <n-icon v-for="index in 6" :key="index" class="star-icon" size="15">
        <star theme="filled" fill="#333" />
      </n-icon>
    </div>
    <img class="portait" alt="Portrait" id="portrait" src="/demo/xusheng-portait.png"/>
    <img class="avatar" alt="Avatar" id="avatar" src="/demo/xusheng-avatar.png"/>
  </div>
</template>

<script lang="ts" setup>

import { Star } from '@icon-park/vue-next'


</script>

<style scoped lang="scss">
.operator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5px;
  border: 1px solid black;
  width: 100px;
  height: 300px;

  .operator-name {
    display: flex;
    flex-direction: row;
    align-items: center;

    .operator-class {
      margin-left: 2px;
      width: 15px;
      height: 15px;
    }
  }


  .rarity {
    display: flex;
    flex-direction: row;
  }

  .portait {
    margin-top: 5px;
    width: 80px;
    height: 160px;
    border: 1px solid black;
  }

  .avatar {
    margin-top: 5px;
    width: 80px;
    height: 80px;
    border: 1px solid black;
  }
}
</style>