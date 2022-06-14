<template>
  <a href="#" class="ms-1" @click="toggleFavoriteCompetitor()">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="icon icon-tabler icon-tabler-star"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      stroke-width="2"
      stroke="#f59f00"
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
  name: 'FavoriteCompetitorStar',
  props: ['userId', 'competitorUuidId'],
  data() {
    return {
      currentState: this.initState,
    }
  },
  mounted() {
    this.isInCompetitorsList()
  },
  methods: {
    async isInCompetitorsList() {
      try {
        const response = await this.$axios.get(`/users/${this.userId}/competitors/`)
        const competitors = response.data.competitors
        const currentPlayerId = this.$route.params.id
        const equalList = competitors.filter(function (e) {
            return e.player_uuid === currentPlayerId
          }
        )
        this.currentState = equalList.length > 0
      } catch (e) {
        console.log(e)
      }
    },
    async toggleFavoriteCompetitor() {
      try {
        this.currentState = !this.currentState
        if (this.currentState) {
          await this.$axios.post(`/users/${this.userId}/competitors/`, {
            player_uuid: this.competitorUuidId,
          })
        } else {
          await this.$axios.delete(
            `/users/${this.userId}/competitors/${this.competitorUuidId}`
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
  fill: #f59f00;
}

.icon-tabler-star {
  width: 1.2rem !important;
  height: 1.2rem !important;
}
</style>
