<template>
  <div class="col-sm-4 col-lg-4">
    <div class="card h-100">
      <div class="card-header">
        <h3 class="card-title">Most Played</h3>
      </div>
      <table class="table card-table table-vcenter">
        <thead>
          <tr>
            <th>Champion</th>
            <th class="text-center">Winrate</th>
            <th class="text-center">Games</th>
          </tr>
        </thead>
        <tbody v-if="playerData">
          <tr
            v-for="champion in playerData.most_played"
            :key="champion.champion_id"
          >
            <td class="p-0">
              <div class="d-flex px-3 align-items-center">
                <span
                  class="avatar avatar-xs avatar-rounded"
                  :style="championIconPath(champion)"
                ></span>
                <div class="flex-fill">
                  <div class="font-weight-medium m-2">
                    <span>{{ champion.champion_name }}</span>
                  </div>
                </div>
              </div>
            </td>
            <td class="text-center">{{ champion.win_rate }} %</td>
            <td class="text-center">{{ champion.games }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerStatsMostPlayed',
  props: ['playerData'],
  methods: {
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
  }
}
</script>
