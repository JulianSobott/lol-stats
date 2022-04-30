<template>
  <div class="input-icon mb-3">
    <input v-bind="playername" v-on:input="searchPlayerName()" type="text" class="form-control" placeholder="Search Player name" />
    <span v-if="searching" class="input-icon-addon">
      <div
        class="spinner-border spinner-border-sm text-muted"
        role="status"
      ></div>
    </span>
  </div>
</template>

<script>
export default {
  name: 'PlayerSearchInput',
  props: [],
  data() {
      return {
        playername: '',
        error: true,
        searching: false,
      }
  },
  methods: {
      searchPlayerName() {
          this.searching = true;
          console.log("changed" + this.playername);
      }
  },
}
</script>
