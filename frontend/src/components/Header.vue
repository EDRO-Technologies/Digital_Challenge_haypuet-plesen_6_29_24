<script setup>
import SurguIcon from "./icons/IconSurgu.vue";
// import SurguIcon from "./assets/Logo Container.svg";
</script>
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <RouterLink class="nav-link active" aria-current="page" to="/"
        ><SurguIcon class="me-2" /><b></b></RouterLink
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto ms-5 mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link active" aria-current="page" to="/"
              >Главная</RouterLink
            >
          </li>
          <!-- <li class="nav-item">
            <RouterLink class="nav-link" aria-current="page" to="/calendar"
              >Мой календарь</RouterLink
            >
          </li> -->
          <li class="nav-item">
            <RouterLink class="nav-link" aria-current="page" to="/create_schedule"
              >Составить расписание</RouterLink
            >
          </li>
          <li class="nav-item">
            <router-link to="/signin" class="nav-link" aria-current="page"
              >Личный кабинет
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
