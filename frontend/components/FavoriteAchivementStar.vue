<template>
  <a href="#" @click="toggleFavoriteAchivement()">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="icon icon-tabler icon-tabler-star"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      stroke-width="2"
      stroke="#fff"
      fill="none"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
      <path
        :class="{ 'icon-tabler-star-active': currentState }"
        d="M12 17.75l-6.172 3.245l1.179 -6.873l-5 -4.867l6.9 -1l3.086 -6.253l3.086 6.253l6.9 1l-5 4.867l1.179 6.873z"
      ></path>
    </svg>
  </a>
</template>

<script>
export default {
  name: 'FavoriteAchivementStar',
  props: ['userId', 'achivementId', 'initState'],
  data() {
    return {
      currentState: this.initState,
    }
  },
  methods: {
    async toggleFavoriteAchivement() {
      try {
        this.currentState = !this.currentState
        if (this.currentState) {
          await this.$axios.post(`/users/${this.userId}/achievements`, {
            id: this.achivementId,
          })
        } else {
          await this.$axios.delete(
            `/users/${this.userId}/achievements/${this.achivementId}`
          )
        }
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>

<style>
.icon-tabler-star-active,
.icon-tabler-star:hover {
  fill: #fff;
}
</style>
