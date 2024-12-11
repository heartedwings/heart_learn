<template>
  <div class="home">
    <div v-if="isLoading" class="overlay">
      <div class="spinner"></div>
      <span>Loading...</span>
    </div>
    <div class="home__main">
      <div class="home__title"><span>心</span>臓病Checker</div>
      <div class="home__graph">
        <div v-for="num in 6" :key="num" class="cell"></div>
      </div>
      <div class="home__contents">
        <div class="home__download">
          <input id="file" type="file" @change="onCsvDownLoad" />
          <button :disabled="!csvFile" @click="saveCsvFile">送信</button>
        </div>
        <div class="home__result--accuracy">
          正解率：{{ resultData ? resultData.accuracy : "-" }}
        </div>
        <Tabs v-model="activeTab">
          <template
            v-for="(name, idx) in tabName"
            :key="idx"
            v-slot:[`tab-${idx}`]
          >
            <div v-show="resultData" class="home__image">
              <img v-if="selectedImage" :src="selectedImage" :alt="name" />
            </div>
            <div v-show="!resultData" class="home__no-image">
              <img src="../assets/no_image.svg" alt="no_image" />
            </div>
          </template>
        </Tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import axios, { AxiosError } from "axios";
import Tabs from "./Tabs.vue";

interface ResultData {
  accuracy: string;
  confusion_matrix: {
    data: Object;
    image: string;
  };
  perm_importance: {
    data: Object;
    image: string;
  };
  shap: {
    image: string;
  };
  learn_curve: {
    image: string;
  };
}

const isLoading = ref(false);
const csvFile = ref<File>();
const resultData = ref<ResultData>();
const activeTab = ref(0);
const tabName = [
  "Confusion Matrix",
  "Permitation Importance",
  "Learn Curve",
  "Shap",
];

const onCsvDownLoad = (event: Event) => {
  const input = event.target as HTMLInputElement;
  csvFile.value = input.files?.[0];
};

// ローカルストレージに画像を保存し、リアクティブに反映させる
const saveImagesToLocalStorage = (images: Record<string, string>) => {
  Object.keys(images).forEach((key) => {
    localStorage.setItem(key, images[key]);
  });
};

// CSVファイルをPOSTし、responseを受け取る
const saveCsvFile = async () => {
  if (!csvFile.value) return;
  const data = new FormData();
  data.append("file", csvFile.value, "test_result.csv");

  isLoading.value = true;
  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/upload_csv",
      data,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );
    resultData.value = response.data.result;

    saveImagesToLocalStorage(response.data.result);
  } catch (error) {
    if (error instanceof AxiosError) {
      console.error("Error response:", error.response?.data || error.message);
    } else {
      console.error("Unexpected Error:", error);
    }
  } finally {
    isLoading.value = false; // ローディング終了
  }
};

// タブのインデックスに基づいて表示する画像を決定
const selectedImage = computed(() => {
  // resultDataがない場合は空文字を返却
  if (!resultData.value) return "";

  switch (activeTab.value) {
    case 0:
      return resultData.value.confusion_matrix.image;
    case 1:
      return resultData.value.perm_importance.image;
    case 2:
      return resultData.value.learn_curve.image;
    case 3:
      return resultData.value.shap.image;
    default:
      return "";
  }
});
</script>

<style lang="scss" scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(128, 128, 128, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border-width: 4px;
  border-style: solid;
  border-color: #fff transparent;
  animation: spin 2s infinite linear forwards;
  &::before {
    content: "";
    position: absolute;
    top: 4px;
    left: 4px;
    right: 4px;
    bottom: 4px;
    border-radius: 50%;
    border-width: 4px;
    border-style: solid;
    border-color: #fff transparent;
    animation: spin 0.7s infinite linear reverse; /* 逆回転 */
  }
}

.home {
  position: relative;
  background-color: #241f1f;
  color: #ffffff;
  min-height: 100vh;

  &__main {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  &__title {
    font-size: 36px;
    margin-top: 16px;
    color: #ffffff;
    text-align: center;

    span {
      color: #d40000;
    }
  }

  &__graph {
    background: linear-gradient(90deg, #242424 0, #af3737 50%, #242424 50%);
    animation: travel 6s infinite linear;
    display: flex;
    margin-top: 16px;
    width: 100%;
    height: 170px;
  }

  .cell {
    display: flex;
    width: 16.7%;
    background: url(https://gistcdn.githack.com/alexmwalker/ab0ffcafbeed4f91756a06531c5cba1d/raw/13a6b6d3b69316a8064f26dd9d341451c34f6bff/hr-with-numbers.svg);
    background-size: 700% auto;
    animation: shuffle 15s steps(1) infinite;
  }

  &__contents {
    max-width: 670px;
    margin: 20px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    input {
      margin: auto 12px;
    }
    img {
      max-height: 500px;
      max-width: 100%;
      object-fit: contain;
      margin: 20px auto;
    }
  }

  &__download {
    display: flex;
    margin-top: 16px;
    button {
      padding: 5px 20px;
      font-size: 16px;
      color: white;
      background-color: #0058b6;
      border: none;
      border-radius: 5px;
      cursor: pointer;

      &:disabled {
        background-color: rgb(144, 144, 144);
        color: #17161640;
        cursor: not-allowed;
      }
    }
  }

  &__result--accuracy {
    margin-top: 32px;
  }

  &__image {
    height: 500px;
    width: 660px;
    margin: auto;
    margin-top: 20px;
    background-color: rgb(255, 255, 255);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  &__no-image {
    height: 500px;
    width: 660px;
    margin: auto;
    margin-top: 20px;
    background-color: rgb(124, 124, 124);
    font-size: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes spinner_loading_text {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes shuffle {
  0%,
  100% {
    background-position: 83.3%, 0;
  }
  16.6% {
    background-position: 33.33%, 0;
  }
  33.3% {
    background-position: 66.66%, 0;
  }
  50% {
    background-position: 16.66%, 0;
  }
  66.6% {
    background-position: 50%, 0;
  }
  83.3% {
    background-position: 0%, 0;
  }
}

@keyframes travel {
  0% {
    background-position: -380px 0;
  }
  100% {
    background-position: 380px 0;
  }
}
</style>
