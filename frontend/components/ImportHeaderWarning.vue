<template>
    <div v-if="$auth.loggedIn && !$auth.user.player_stats.imported" class="d-block w-100 text-center bg-red">
        <div class="p-2">Your player data is being imported! Please wait...</div>
    </div>
</template>