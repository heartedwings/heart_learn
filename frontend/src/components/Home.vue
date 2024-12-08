<template>
  <div class="home__main">
    <div class="home__title">心臓病確認</div>
    <div class="home__contents">
      <input id="file" type="file" @change="onCsvDownLoad" />
      <button class="home__button" :disabled="!csvFile" @click="saveCsvFile">
        送信
      </button>
      <div v-if="resultData">
        <div>正解率：{{ resultData.result.accuracy }}</div>
        <div>
          混同行列
          <div>{{ resultData.result.confusion_matrix.data[0] }}</div>
          <div>{{ resultData.result.confusion_matrix.data[1] }}</div>
          <div>
            <img :src=resultData.result.confusion_matrix.image />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

axios.defaults.headers.get["Content-Type"] = "application/json";
axios.defaults.headers.get["Access-Control-Allow-Origin"] = "*";

// defineProps<{ msg: string }>();

const csvFile = ref<File>();
// const accuracy = ref<number>(0.88);
const resultData = ref();

const onCsvDownLoad = (event: Event) => {
  console.log(event);
  if (!event.target) return;
  const input = event.target as HTMLInputElement;
  console.log(input.files?.[0]);
  csvFile.value = input.files?.[0];
};

const saveCsvFile = async () => {
  console.log("送信", csvFile.value);
  if (!csvFile.value) return;
  // CSVデータを Blob に変換
  const blob = new Blob([csvFile.value], { type: "text/csv" });
  console.log(blob);

  const data = new FormData();
  data.append("file", blob, "test_result.csv");

  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/upload_csv",
      data,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token",
        },
      }
    );
    resultData.value = response.data;
    console.log(response.data);
    console.log(resultData.value);
  } catch (error: any) {
    console.error(
      "Error:",
      error.response ? error.response.data : error.message
    );
  }
};
</script>

<style lang="scss" scoped>
.home {
  &__title {
    font-size: 36px;
  }
}
</style>
