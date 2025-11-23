<script setup></script>

<template>
  <div class="row m-0 my-5 justify-content-center">
    <div class="p-4 col-sm-8 col-md-6 col-xl-4 rounded-3 shadow-sm">
      <form @submit.prevent>
        <div class="text-center">
          <label for="InputData" class="form-label h3"
            ><div>Регистрация</div></label
          >
        </div>
        <div class="form-floating mb-3">
          <input
            v-model="first_name"
            type="name"
            class="form-control"
            id="first_name"
            placeholder=""
          />
          <label for="floatingInput"> Имя </label>
        </div>
        <div class="form-floating mb-3">
          <input
            v-model="second_name"
            type="name"
            class="form-control"
            id="second_name"
            placeholder=""
          />
          <label for="floatingInput"> Фамилия </label>
        </div>
        <div class="form-floating mb-3">
          <input
            v-model="middle_name"
            type="name"
            class="form-control"
            id="middle_name"
            placeholder=""
          />
          <label for="floatingInput"> Отчество (при наличии ) </label>
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
          <label for="floatingInput"> Email* </label>
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
          <label for="floatingInput"> Пароль* </label>
        </div>
        <div class="form-floating mb-3">
          <input
            v-model="password2"
            type="password"
            class="form-control"
            id="password2"
            placeholder=""
            required
          />
          <label for="floatingInput"> Повторите пароль* </label>
        </div>
        <div class="mb-3 form-check">
          <input
            v-model="agreementCheckBox"
            type="checkbox"
            class="form-check-input"
            id="agreement"
            required
          />
          <label class="form-check-label" for="agreement"
            >Согласие на обработку персональных данных*</label
          >
        </div>
        <div
          v-if="error"
          class="alert alert-warning alert-dismissible fade show"
          role="alert"
        >
          <strong>Что-то пошло не так!</strong> {{ error }}
        </div>

        <div class="text-center mb-3">
          <button
            type="submit"
            class="btn btn-primary col-8"
            style="height: 50px"
            @click="authorisation"
          >
            <Loader v-if="loader" />
            <div v-else>Зарегистрироваться</div>
          </button>
        </div>

        <div class="text-center">
          <router-link to="/signin">Уже есть аккаунт?</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
