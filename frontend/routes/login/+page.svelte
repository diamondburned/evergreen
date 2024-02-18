<script lang="ts">
  import RegistrationPage from "$lib/components/RegistrationPage.svelte";
  import { isLoggedIn, login, token } from "$lib/api";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";

  async function submit() {
    const session = await login({ email, password });
    $token = session.token;
    $isLoggedIn = true;
    goto("/");
  }
</script>

<svelte:head>
  <title>Sign in</title>
</svelte:head>

<RegistrationPage {submit} submitLabel="Sign in" valid={!!(email && password)}>
  <label>
    Email
    <input type="email" bind:value={email} />
  </label>
  <label>
    Password
    <input type="password" bind:value={password} />
  </label>
</RegistrationPage>
