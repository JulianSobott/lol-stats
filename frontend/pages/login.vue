<template>
<div class="page page-center">
  <div class="container-tight py-4">
    <div class="text-center mb-4">
      <a href="." class="navbar-brand navbar-brand-autodark">LOL Stats</a>
    </div>
    <form>
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Login to your account</h2>
        <div class="mb-3">
          <label class="form-label">Email address</label>
          <input v-model="email" type="email" class="form-control" placeholder="Enter email">
        </div>
        <div class="mb-2">
          <label class="form-label">
            Password
          </label>
          <div class="input-group input-group-flat">
            <input v-model="password" type="password" class="form-control"  placeholder="Password"  autocomplete="off">
            <span class="input-group-text">
              <a href="#" class="link-secondary" title="Show password" data-bs-toggle="tooltip"><!-- Download SVG icon from http://tabler-icons.io/i/eye -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="12" cy="12" r="2" /><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7" /></svg>
              </a>
            </span>
          </div>
        </div>
        <div class="mb-2">
          <label class="form-check">
            <input type="checkbox" class="form-check-input"/>
            <span class="form-check-label">Remember me on this device</span>
          </label>
        </div>
        <div class="form-footer">
          <button class="btn btn-primary w-100" @click="login()">Sign in</button>
        </div>
      </div>
    </form>
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
      email: '',
      password: '',
      error: null
    }
  },
  head: {
    bodyAttrs: {
      class: 'theme-dark border-top-wide border-primary d-flex flex-column'
    }
  },
  methods: {
    login() {
      this.$router.push('/');
    }
  }

}
</script>
