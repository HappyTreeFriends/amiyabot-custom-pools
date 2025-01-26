<template>
  <n-popover trigger="hover" :show-arrow="false" placement="right">
    <template #trigger>
      <n-button
        size="small"
        @click="handleClick"
        class="operator-button"
        style="width: 110px; height: 50px;"
      >
        <n-flex vertical align="center">
          <div class="operator-name">
            <n-ellipsis style="max-width: 70px; margin-right: 4px;">{{ operatorData.name }}</n-ellipsis>
            <n-image
              width="15"
              height="15"
              :src="getClassImage(operatorData.class)"
              preview-disabled
            />
          </div>
          
          <div class="rarity">
            <n-icon
              v-for="index in operatorData.rarity"
              :key="index"
              size="15"
              color="#333"
            >
              <star theme="filled" />
            </n-icon>
            <n-icon
              v-for="index in 6-operatorData.rarity"
              :key="index"
              size="15"
              color="#333"
            >
              <star />
            </n-icon>
          </div>
        </n-flex>
      </n-button>
    </template>

      <div class="operator-popup">
        <!-- <span class="operator-name-full">假日威龙陈假日威龙陈假日威龙陈假日威龙陈</span> -->
        <n-image
          width="80"
          height="160"
          :src="operatorData.portrait"
          style="border: 1px solid black; margin-bottom: 10px;"
          preview-disabled
        />
        <n-image
          width="80"
          height="80"
          :src="operatorData.avatar"
          style="border: 1px solid black;"
          preview-disabled
        />
      </div>
  </n-popover>
</template>

<script lang="ts" setup>
import { Star } from '@icon-park/vue-next'
import { defineEmits, defineProps } from 'vue'
import {getClassImage} from '@/utils/classes'

interface OperatorData {
  [key: string]: any
}

const props = defineProps<{
  operatorData: OperatorData  // 必选参数
}>()

// 定义组件事件
const emit = defineEmits<{
  (e: 'click', data: OperatorData): void
}>()

const handleClick = () => {
  console.log('click',props.operatorData)
  emit('click', props.operatorData)
}
</script>

<style scoped>

.operator-button {
  margin: 2px;
}

.operator-name {
  display: flex;
  flex-direction: row;
}

.operator-name-full {
  width: 80px;
  margin-bottom: 4px;
  white-space: pre-line;
}

.rarity {
    display: flex;
    flex-direction: row;
  }

.operator-popup {
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>