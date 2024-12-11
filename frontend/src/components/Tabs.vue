<template>
  <div class="tabs">
    <ul class="tab-list">
      <li
        v-for="(tab, index) in tabs"
        :key="index"
        :class="{ active: activeTab === index }"
        @click="selectTab(index)"
      >
        {{ tab }}
      </li>
    </ul>
    <div class="tab-content">
      <slot :name="`tab-${activeTab}`"></slot>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
  },
});

const emits = defineEmits(["update:modelValue"]);

const tabs = [
  "Confusion Matrix",
  "Permitation Importance",
  "Learn Curve",
  "Shap",
];
const activeTab = ref(props.modelValue);

const selectTab = (index: number) => {
  activeTab.value = index;
  emits("update:modelValue", index);
};

watch(
  () => props.modelValue,
  (newVal) => {
    activeTab.value = newVal;
  }
);
</script>

<style scoped>
.tabs {
  display: flex;
  flex-direction: column;
}

.tab-list {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
  margin: 0;
}

.tab-list li {
  flex: 1 1 auto;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.tab-list li.active {
  font-weight: bold;
  border-bottom: 2px solid #999999;
}

.tab-list li img {
  width: 20px; /* 画像の幅を文字の幅に調整 */
  height: auto; /* アスペクト比を保つ */
  margin-left: 10px; /* 文字と画像の間にスペースを追加 */
}

@media (max-width: 600px) {
  .tab-list li {
    padding: 5px 10px;
  }

  .tab-list li img {
    width: 16px; /* 画像の幅を縮小 */
    margin-left: 5px;
  }
}
</style>
