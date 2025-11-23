<script setup>
import { RouterLink, RouterView } from "vue-router";
import Header from "./components/Header.vue";
</script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <Header />
    <div class="container px-4 py-5">
      <RouterView />
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
table .w-10 {
  width: 10%;
}
table .w-15 {
  width: 15%;
}
table .w-20 {
  width: 20%;
}
</style>
