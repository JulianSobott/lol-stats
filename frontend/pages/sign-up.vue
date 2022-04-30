<template>
<div class="page page-center">
  <form class="container-tight py-4"  @submit.prevent="login" >
    <div class="text-center mb-4">
      <NuxtLink to="/login">
        <img src="~/assets/images/logo.png" height="36"/>
      </NuxtLink>
    </div>
    <div class="card card-md">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Create new account</h2>
        <div class="mb-3">
          <label class="form-label required">Email address</label>
          <input v-model="form.email" type="email" class="form-control" :class="{ 'is-invalid': submitted && $v.form.email.$error }" placeholder="Enter email" required>
          <div v-if="submitted && !$v.form.email.required" class="invalid-feedback d-block">Email is required</div>
          <div v-if="submitted && !$v.form.email.email" class="invalid-feedback d-block">Email is invalid</div>
        </div>
        <div class="mb-3">
          <label class="form-label required">Password</label>
          <div class="input-group input-group-flat">
            <input v-model="form.password" type="password" class="form-control" :class="{ 'is-invalid': submitted && $v.form.password.$error }" name="password" placeholder="Password" autocomplete="off" required>
          </div>
          <div v-if="submitted && !$v.form.password.required" class="invalid-feedback d-block">Password is required</div>
          <div v-if="submitted && !$v.form.password.minLength" class="invalid-feedback d-block">Password must be at least 6 characters</div>
        </div>
        <div class="mb-3">
          <label class="form-label required">Confirm Password</label>
          <div class="input-group input-group-flat">
            <input v-model="form.confirmPassword" type="password" class="form-control" :class="{ 'is-invalid': submitted && $v.form.confirmPassword.$error }" name="confirm-password"  placeholder="Password" autocomplete="off" required>
          </div>
          <div v-if="submitted && !$v.form.confirmPassword.required" class="invalid-feedback d-block">Confirm Password is required</div>
          <div v-if="submitted && !$v.form.confirmPassword.sameAsPassword" class="invalid-feedback d-block">Passwords must match</div>
        </div>
        <div class="form-footer">
          <button type="submit" class="btn btn-primary w-100" @click="login">Create new account</button>
        </div>
      </div>
    </div>
    <div class="text-center text-muted mt-3">
      Already have account? <a href="/login" tabindex="-1">Sign in</a>
    </div>
  </form>
</div>
</template>

<script>
import { required, email, sameAs, minLength, } from 'vuelidate/lib/validators'

export default {
  name: 'SignUpPage',
  data() {
    return {
      form: {
        email: '',
        password: '',
        confirmPassword: '',
        error: null
      },
      submitted: false
    }
  },
  head: {
    bodyAttrs: {
      class: 'theme-dark border-top-wide border-primary d-flex flex-column'
    }
  },
  validations: {
    form: {
      email: {
        required,
        email
      },
      password: {
        required,
        minLength: minLength(6)
      },
      confirmPassword: {
        required,
        sameAsPassword: sameAs('password')
      },
    },
  },
  methods: {
    login() {
      this.submitted = true;
      
      this.$v.$touch();
      if (this.$v.$invalid) {
          return;
      }

      this.$router.push('/setup');
    }
  }

}
</script>
