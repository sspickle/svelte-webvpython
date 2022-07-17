import { writable } from 'svelte/store'

export interface User {
  email: string
  name: string
  imageUrl: string
}

export const currentUser = writable<User>()

export function handelAuthIn() {
  gapi.auth2.getAuthInstance().signIn()
}

export function handleSignOut() {
  gapi.auth2.getAuthInstance().signOut()
}

export function setCurrentUser(isSignedIn: boolean) {
  if (isSignedIn) {
    const profile = gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile()
    currentUser.set({
      email: profile.getEmail(),
      name: profile.getName(),
      imageUrl: profile.getImageUrl()
    })
  } else {
    currentUser.set(undefined)
  }
}