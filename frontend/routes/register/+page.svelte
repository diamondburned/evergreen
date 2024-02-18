<script lang="ts">
  import RegistrationPage from "$lib/components/RegistrationPage.svelte";
  import { isLoggedIn, registerSession, token } from "$lib/api";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let preferredName = "";
  $: valid = !!(email && password && preferredName);

  async function submit() {
    await registerSession({ email, password, display_name: preferredName });
    $isLoggedIn = true;
    goto("/");
  }
</script>

<svelte:head>
  <title>Sign up</title>
</svelte:head>

<RegistrationPage {submit} submitLabel="Sign up" {valid}>
  <label>
    Preferred Name
    <input type="text" bind:value={preferredName} />
  </label>
  <label>
    Email
    <input type="email" bind:value={email} />
  </label>
  <label>
    Password
    <input type="password" bind:value={password} />
  </label>
</RegistrationPage>
