<script lang="ts">
  import Hero from "./../../lib/components/Hero.svelte";
  import { token, login } from "$lib/api";
  import { goto } from "$app/navigation";
  import NavBar from "$lib/components/NavBar.svelte";
  import ErrorMessage from "$lib/components/ErrorMessage.svelte";

  export let submit: () => Promise<void>;
  export let submitLabel: string;
  export let valid: boolean;

  let error: string | undefined = undefined;
</script>

<svelte:head>
  <title>Login</title>
</svelte:head>

<Hero>
  <header>
    <NavBar navigation={[]} />
  </header>

  <main>
    <form>
      <ErrorMessage {error} />
      <slot />
      <button
        class="floaty inverted"
        disabled={!valid}
        on:click={async () => {
          error = undefined;
          try {
            await submit();
          } catch (err) {
            error = `${err}`;
          }
        }}
      >
        {submitLabel}
      </button>
    </form>
  </main>
</Hero>

<style lang="scss">
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  main,
  header {
    position: absolute;
  }

  main {
    width: 100%;
    height: 100%;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 2rem;

    :global(label) {
      width: 100%;
      max-width: 300px;

      display: flex;
      flex-direction: column;

      font-size: 0.95em;
      font-weight: 700;
      font-family: "Linotte", sans-serif;

      :global(input) {
        margin-top: 0.25em;
        padding: 0.5em;
        border: 1px solid var(--primary);
        border-radius: 15px;
      }
    }

    button {
      width: fit-content;
      margin: auto;
      padding: 0.5em 2em;

      border-radius: 15px;
      transition: all 0.15s linear;

      &:hover {
        box-shadow: 0 0.5em 0.5em -0.4em var(--md-sys-color-shadow);
      }
    }
  }
</style>
