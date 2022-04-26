<template>
<div class="page page-center">
  <div class="container-tight py-4">
    <div class="text-center mb-4">
      <NuxtLink to="/login">
        <img src="~/assets/images/logo.png" height="36"/>
      </NuxtLink>
    </div>
    <div class="card card-md">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Login to your account</h2>
        <div class="mb-3">
          <label class="form-label">Email address</label>
          <input v-model="form.email" type="email" class="form-control" :class="{ 'is-invalid': submitted && error }" placeholder="Enter email">
        </div>
        <div class="mb-2">
          <label class="form-label">
            Password
          </label>
          <div class="input-group input-group-flat">
            <input v-model="form.password" type="password" class="form-control"  :class="{ 'is-invalid': submitted && error }" placeholder="Password"  autocomplete="off">
          </div>
        </div>
        <div v-if="submitted && error" class="invalid-feedback d-block mb-2">E-Mail or password wrong</div>
        <div class="form-footer">
          <button class="btn btn-primary w-100" @click="login()">Sign in</button>
        </div>
      </div>
    </div>
    <div class="text-center text-muted mt-3">
      Don't have account yet? <a href="sign-up" tabindex="-1">Sign up</a>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      submitted: false,
      error: null
    }
  },
  head: {
    bodyAttrs: {
      class: 'theme-dark border-top-wide border-primary d-flex flex-column'
    }
  },
  methods: {
    async login() {
      this.submitted = true;
      this.error = true;

      try {
        const response = await this.$auth.loginWith('local', { data: this.form })
        console.log(response)
      } catch (err) {
        console.log(err)
      }
    }
  }
}
</script>
