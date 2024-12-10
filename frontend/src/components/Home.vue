<template>
  <div class="home">
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
        <div v-if="resultData">
          <img :src="resultData.image" alt="Confusion Matrix" />
        </div>
        <div class="home__no-image" v-else>
          <img src="../assets/no_image.svg" alt="no_image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios, { AxiosError } from "axios";

interface ResultData {
  accuracy: string;
  confusion_matrix: Array<string>;
  image: string;
}

const csvFile = ref<File>();
const resultData = ref<ResultData>();

const onCsvDownLoad = (event: Event) => {
  const input = event.target as HTMLInputElement;
  csvFile.value = input.files?.[0];
};

// ローカルストレージに画像を保存し、リアクティブに反映させる
const saveImageToLocalStorage = (imageBase64: string) => {
  localStorage.setItem("image", imageBase64);
  if (resultData.value) resultData.value.image = imageBase64;
};

// CSVファイルをPOSTし、responseを受け取る
const saveCsvFile = async () => {
  if (!csvFile.value) return;
  const data = new FormData();
  data.append("file", csvFile.value, "test_result.csv");

  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/upload_csv",
      data,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );
    resultData.value = response.data.result;
    saveImageToLocalStorage(response.data.result.confusion_matrix.image);
  } catch (error) {
    if (error instanceof AxiosError) {
      console.error("Error response:", error.response?.data || error.message);
    } else {
      console.error("Unexpected Error:", error);
    }
  }
};
</script>

<style lang="scss" scoped>
.home {
  position: relative;
  background-color: #241f1f;
  color: #ffffff;
  height: 100vh;
  overflow: hidden;

  &__main {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    margin: 20px 16px 32px 16px;
    overflow: hidden;
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
    height: 200px;
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
    margin-top: 20px;
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
    margin-top: 16px;
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
