<template>
    <n-card class="game-info">
        <n-space justify="space-between" >
            <n-space>
                <img class="game-logo" src="" alt="" />
                <div>
                    <div style="font-size: 16px; font-weight: bold">
                        {{  }}
                    </div>
                    <n-button text>
                        <div style="font-size: 12px; color: #898989">#{{  }}</div>
                    </n-button>
                </div>
            </n-space>
            <div class="buttons">
                <slot name="tags"></slot>
                <n-tag type="primary" v-if="true">私人房间</n-tag>
                <n-tag type="success" v-else>公开房间</n-tag>
                <n-tag type="info">查看规则</n-tag>
            </div>
        </n-space>
        <div class="game-actions" style="margin-top: 20px">
            <slot name="buttons"></slot>
        </div>
    </n-card>
</template>

<script lang="ts" setup>

</script>

<style lang="scss">
.game-info {
    .game-logo {
        width: 50px;
        border-radius: 4px;
    }

    .buttons{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;

        @media (min-width: 360px) {
            flex-direction: row;
        }
    }

    .game-actions {
        display: flex;

        & > button {
            flex: 2;

            &:not(:last-child) {
                margin-right: 10px;
            }
        }
    }
}

</style>
