<template>
  <form ref="filters" class="achievement-filters">
    <div class="mb-3">
      <label class="form-label subheader mb-2">Compare with</label>
      <div>
        <label class="form-check mb-1">
          <input
            v-model="filters.compare"
            type="radio"
            class="form-check-input"
            value="global"
            @change="globalAndCompetitorsRadioSelected()"
          />
          <span class="form-check-label">Global</span>
        </label>
        <label class="form-check mb-1">
          <input
            v-model="filters.compare"
            type="radio"
            class="form-check-input"
            value="competitors"
            @change="globalAndCompetitorsRadioSelected()"
          />
          <span class="form-check-label">Competitors</span>
        </label>
        <label class="form-check mb-1">
          <input
            v-model="filters.compare"
            type="radio"
            class="form-check-input"
            value="player"
            @change="playerRadioSelected()"
          />
          <span class="form-check-label">Player</span>
        </label>
      </div>
    </div>
    <div class="form-group mb-3" :class="{'d-none': !displayPlayerSearch}">
      <label class="form-label subheader mb-2">Player</label>
      <PlayerSearchInput
        class="mb-3"
        ref="PlayerSearchInput"
        @playerSelected="playerChanged"
      />
    </div>
    <div class="form-group mb-3 d-none">
      <label class="form-label subheader mb-2">Champion</label>
      <div>
        <select v-model="filters.champion" class="form-select">
          <option value="*">All Champions</option>
          <option v-for="champ in allChampions" :key="champ" :value="champ">
            {{ champ }}
          </option>
        </select>
      </div>
    </div>
    <div class="form-group mb-3">
      <label class="form-label subheader mb-2">Rank</label>
      <div>
        <select v-model="filters.rank" class="form-select">
          <option value="*">All Ranks</option>
          <option value="iron">Iron</option>
          <option value="bronze">Bronze</option>
          <option value="silver">Silver</option>
          <option value="gold">Gold</option>
          <option value="platinum">Platinum</option>
          <option value="diamond">Diamond</option>
          <option value="master">Master</option>
          <option value="grandmaster">Grandmaster</option>
          <option value="challenger">Challenger</option>
        </select>
      </div>
    </div>
    <div class="mt-4">
      <button
        class="btn btn-primary w-100"
        data-bs-dismiss="offcanvas"
        :disabled="!canSubmit"
        @click="search"
      >
        Confirm changes
      </button>
      <a class="btn btn-link w-100" @click="clearFilters">
        Reset to defaults
      </a>
    </div>
  </form>
</template>

<script>
export default {
  name: 'AchievementFilters',
  data() {
    return {
      canSubmit: true,
      displayPlayerSearch: false,
      filters: {
        compare: 'global',
        player: null,
        champion: '*',
        rank: '*',
      },
      allChampions: [
        'Aatrox',
        'Ahri',
        'Akali',
        'Akshan',
        'Alistar',
        'Amumu',
        'Anivia',
        'Annie',
        'Aphelios',
        'Ashe',
        'Aurelion Sol',
        'Azir',
        'Bard',
        'Blitzcrank',
        'Brand',
        'Braum',
        'Caitlyn',
        'Camille',
        'Cassiopeia',
        'Cho Gath',
        'Corki',
        'Darius',
        'Diana',
        'Draven',
        'Dr. Mundo',
        'Ekko',
        'Elise',
        'Evelynn',
        'Ezreal',
        'Fiddlesticks',
        'Fiora',
        'Fizz',
        'Galio',
        'Gangplank',
        'Garen',
        'Gnar',
        'Gragas',
        'Graves',
        'Gwen',
        'Hecarim',
        'Heimerdinger',
        'Illaoi',
        'Irelia',
        'Ivern',
        'Janna',
        'Jarvan IV',
        'Jax',
        'Jayce',
        'Jhin',
        'Jinx',
        'Kai Sa',
        'Kalista',
        'Karma',
        'Karthus',
        'Kassadin',
        'Katarina',
        'Kayle',
        'Kayn',
        'Kennen',
        'Kha Zix',
        'Kindred',
        'Kled',
        'Kog Maw',
        'LeBlanc',
        'Lee Sin',
        'Leona',
        'Lillia',
        'Lissandra',
        'Lucian',
        'Lulu',
        'Lux',
        'Malphite',
        'Malzahar',
        'Maokai',
        'Master Yi',
        'Miss Fortune',
        'Wukong',
        'Mordekaiser',
        'Morgana',
        'Nami',
        'Nasus',
        'Nautilus',
        'Neeko',
        'Nidalee',
        'Nocturne',
        'Nunu & Willump',
        'Olaf',
        'Orianna',
        'Ornn',
        'Pantheon',
        'Poppy',
        'Pyke',
        'Qiyana',
        'Quinn',
        'Rakan',
        'Rammus',
        'Rek Sai',
        'Rell',
        'Renata Glasc',
        'Renekton',
        'Rengar',
        'Riven',
        'Rumble',
        'Ryze',
        'Samira',
        'Sejuani',
        'Senna',
        'Seraphine',
        'Sett',
        'Shaco',
        'Shen',
        'Shyvana',
        'Singed',
        'Sion',
        'Sivir',
        'Skarner',
        'Sona',
        'Soraka',
        'Swain',
        'Sylas',
        'Syndra',
        'Tahm Kench',
        'Taliyah',
        'Talon',
        'Taric',
        'Teemo',
        'Thresh',
        'Tristana',
        'Trundle',
        'Tryndamere',
        'Twisted Fate',
        'Twitch',
        'Udyr',
        'Urgot',
        'Varus',
        'Vayne',
        'Veigar',
        'Vel Koz',
        'Vex',
        'Vi',
        'Viego',
        'Viktor',
        'Vladimir',
        'Volibear',
        'Warwick',
        'Xayah',
        'Xerath',
        'Xin Zhao',
        'Yasuo',
        'Yone',
        'Yorick',
        'Yuumi',
        'Zac',
        'Zed',
        'Zeri',
        'Ziggs',
        'Zilean',
        'Zoe',
        'Zyra',
      ],
    }
  },
  mounted() {
    this.$refs.PlayerSearchInput.disable(true)

    if (this.$route.query.playername !== undefined) {
      this.filters.compare = 'player'
      this.$refs.PlayerSearchInput.setPlayerData(
         this.$route.query.playername,
        null
      )
      this.displayPlayerSearch = true
      this.$refs.PlayerSearchInput.disable(false)
    }
  },
  methods: {
    search(e) {
      this.$emit('filterApplied', { ...this.filters })
      e.preventDefault()
    },
    playerChanged(playerData) {
      this.filters.player = playerData
      this.canSubmit = playerData != null
    },
    clearFilters() {
      this.$refs.PlayerSearchInput.clear()
      this.filters = {
        compare: 'global',
        player: null,
        champion: '*',
        rank: '*',
      }
      this.canSubmit = true
      this.displayPlayerSearch = false
    },
    playerRadioSelected() {
      this.$refs.PlayerSearchInput.disable(false)
      this.displayPlayerSearch = true
      if(this.filters.player === null) {
        this.canSubmit = false
      }
    },
    globalAndCompetitorsRadioSelected() {
      this.$refs.PlayerSearchInput.disable(true)
      this.displayPlayerSearch = false
      this.canSubmit = true
    },
  },
}
</script>
