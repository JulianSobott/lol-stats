<template>
  <div
    id="achivement-filters"
    class="offcanvas offcanvas-start"
    tabindex="-1"
    aria-labelledby="achivement-filters-label"
    style="visibility: hidden"
    aria-hidden="true"
  >
    <div class="offcanvas-header">
      <h2 id="achivement-filters-label" class="offcanvas-title">Achivement Filters</h2>
      <button
        type="button"
        class="btn-close text-reset"
        data-bs-dismiss="offcanvas"
        aria-label="Close"
      ></button>
    </div>
    <div class="offcanvas-body">
        <AchievementFilters />
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidebarAchievementFilters',
}
</script>
