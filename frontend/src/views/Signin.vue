<script setup></script>

<template>
  <div class="row m-0 my-5 justify-content-center">
    <div class="p-4 col-sm-8 col-md-6 col-xl-4 rounded-3 shadow-sm">
      <form @submit.prevent>
        <div class="text-center">
          <label for="InputData" class="form-label h3"><div>Вход</div></label>
        </div>

        <div class="form-floating mb-3">
          <input
            v-model="username"
            type="email"
            class="form-control"
            id="username"
            placeholder=""
            required
          />
          <label for="floatingInput"> Email </label>
        </div>
        <div class="form-floating mb-3">
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
            placeholder=""
            required
          />
          <label for="floatingInput"> Пароль </label>
        </div>
        <div
          v-if="error"
          class="alert alert-warning alert-dismissible fade show"
          role="alert"
        >
          <strong>Что-то пошло не так!</strong> {{ authStore.error }}
        </div>

        <div class="text-center mb-3">
          <Loader v-if="loader" />
          <button
            v-else
            type="submit"
            class="btn btn-primary col-8"
            style="height: 50px"
            @click="authorisation"
          >
            <div>Войти</div>
          </button>
        </div>

        <div class="text-center">
          <router-link to="/signup">Еще нет аккаунта?</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
