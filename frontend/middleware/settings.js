export default function ({ store, redirect }) {
    if (store.state.auth.loggedIn) {
      if(store.state.auth.user.player_uuid === null) {
        return redirect('/settings?firstsetup=true')
      }
    }
  }