import { ref } from "vue";

export const currentUser = ref(null);

export function setCurrentUser(user) {
  currentUser.value = user || null;
}
