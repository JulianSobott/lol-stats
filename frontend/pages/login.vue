<template>
  <div class="page page-center">
    <div class="container-tight py-4">
      <div class="text-center mb-4">
        <NuxtLink to="/login">
          <img src="~/assets/images/logo.png" height="36" />
        </NuxtLink>
      </div>
      <div class="card card-md">
        <div v-if="error" class="card-status-top bg-danger"></div>
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Login to your account</h2>
          <p v-if="logoutSuccess" class="card-subtitle text-green text-center">
            You have been logged out successfully.
          </p>
          <div class="mb-3">
            <label class="form-label">Email address</label>
            <input
              v-model="form.email"
              type="email"
              class="form-control"
              :class="{ 'is-invalid': submitted && error }"
              placeholder="Enter email"
            />
            <div
              v-if="submitted && !$v.form.email.required"
              class="invalid-feedback d-block"
            >
              Email is required
            </div>
          </div>
          <div class="mb-2">
            <label class="form-label"> Password </label>
            <div class="input-group input-group-flat">
              <input
                v-model="form.password"
                type="password"
                class="form-control"
                :class="{ 'is-invalid': submitted && error }"
                placeholder="Password"
                autocomplete="off"
              />
              <div
                v-if="submitted && !$v.form.password.required"
                class="invalid-feedback d-block"
              >
                Password is required
              </div>
            </div>
          </div>
          <div v-if="submitted && error" class="invalid-feedback d-block mb-2">
            E-Mail or password wrong
          </div>
          <div class="form-footer">
            <button class="btn btn-primary w-100" @click="login()">
              Sign in
            </button>
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
import { required } from 'vuelidate/lib/validators'
import { mapActions } from 'vuex'

export default {
  name: 'LoginPage',
  mounted() {
    if (this.$route.query.logout !== undefined) {
      this.logoutSuccess = this.$route.query.logout === 'true'
    } else {
      this.logoutSuccess = false
    }
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      submitted: false,
      error: null,
      logoutSuccess: false,
    }
  },
  head: {
    bodyAttrs: {
      class: 'theme-dark border-top-wide border-primary d-flex flex-column',
    },
  },
  validations: {
    form: {
      email: {
        required,
      },
      password: {
        required,
      },
    },
  },
  methods: {
    ...mapActions({
      clearStore: 'dashboard/clearStore',
    }),
    async login() {
      this.submitted = true
      this.error = false

      this.$v.$touch()
      if (this.$v.$invalid) {
        this.error = true
        return
      }

      this.clearStore()

      try {
        await this.$auth
          .loginWith('local', {
            data: {
              email: this.form.email,
              password: this.form.password,
            },
          })
          .then(() => {
            this.$auth.fetchUser()
            if (this.$auth.user.player_uuid === null) {
              this.$router.push('/settings?firstsetup=true')
            } else {
              this.$router.push('/dashboard?welcome=true')
            }
          })
      } catch (err) {
        this.error = true
      }
    },
  },
}
</script>
