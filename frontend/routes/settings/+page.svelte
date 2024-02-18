<script lang="ts">
  import { onMount } from "svelte";
  import NavBar from "$lib/components/NavBar.svelte";
  import WhitePage from "$lib/components/WhitePage.svelte";
  import ErrorMessage from "$lib/components/ErrorMessage.svelte";
  import {
    uploadAsset,
    getSelf,
    updateSelf as updateSelfAPI,
    type UserResponse,
    type UpdateUserRequest,
  } from "$lib/api";

  let self: UserResponse;
  $: isAnonymous = !self || self.email === null;

  let busy = false;
  let error: string | undefined;

  let files: FileList;

  let password: string;
  let passwordConfirmation: string;
  $: confirmedPassword = !!password && password === passwordConfirmation;

  let displayNameChanged = false;
  let showEmailnput = false;
  let showPasswordInput = false;

  // updateSelf wraps the updateSelfAPI function and handles the busy state and
  // error handling.
  async function updateSelf(data: UpdateUserRequest) {
    busy = true;
    error = undefined;
    try {
      self = await updateSelfAPI(data);
    } catch (err) {
      error = `${err}`;
      console.error(err);
    } finally {
      busy = false;
    }
  }

  async function setAvatar() {
    if (!files) return;
    const avatar = await uploadAsset({ file: files[0]!.slice() });
    await updateSelf({ avatar_hash: avatar.hash });
  }

  async function displayNameButtonPressed() {
    if (!displayNameChanged) {
      displayNameChanged = true;
      return;
    }

    displayNameChanged = false;
    await updateSelf({ display_name: self.display_name });
  }

  async function emailButtonPressed() {
    if (!showEmailnput) {
      showEmailnput = true;
      return;
    }

    showEmailnput = false;
    await updateSelf({ email: self.email });
  }

  async function passwordButtonPressed() {
    if (!showPasswordInput) {
      showPasswordInput = true;
      return;
    }

    showPasswordInput = false;
    await updateSelf({ password });
  }

  onMount(async () => {
    self = await getSelf();
  });
</script>

<svelte:head>
  <title>Settings</title>
</svelte:head>

<WhitePage>
  <section class="container">
    <h2>Settings</h2>

    <form class="settings">
      {#if !self}
        <p class="loading">Loading...</p>
      {:else if isAnonymous}
        <h3>Warning</h3>
        <p>You are currently an anonymous user. You can create an account to save your settings.</p>
        <p>
          To create an account, head to the <a href="/register">signup page</a>.
        </p>
      {:else if self}
        <ErrorMessage bind:error />

        <formset class="avatar">
          <h3>Avatar</h3>
          <div class="user">
            <img
              src={self.avatar_hash ? `/api/assets/${self.avatar_hash}` : `/stock-avatar.jpeg`}
              alt="Avatar"
              class="avatar"
            />
            <div role="group">
              <input type="file" bind:files accept=".jpg, jpeg, .png, .webp" disabled={busy} />
              <button
                class="large floaty inverted"
                type="submit"
                on:click={setAvatar}
                disabled={busy || !files}
              >
                Save
              </button>
            </div>
          </div>
        </formset>

        <formset class="display-name">
          <h3>Display Name</h3>
          <div class="user">
            <input
              bind:value={self.display_name}
              on:input={() => (displayNameChanged = true)}
              disabled={busy}
            />
            <button
              class="large floaty inverted"
              type="submit"
              on:click={displayNameButtonPressed}
              disabled={busy || !displayNameChanged}
            >
              Save
            </button>
          </div>
        </formset>

        <formset class="email">
          <h3>Email:</h3>
          <div class="user">
            {#if showEmailnput}
              <input bind:value={self.email} />
            {:else}
              <p>
                {#if self.email}
                  {self.email}
                {:else}
                  <em>No email set for anonymous user</em>
                {/if}
              </p>
            {/if}
            <button
              class="large floaty inverted"
              type="submit"
              on:click={emailButtonPressed}
              disabled={busy}
            >
              {#if showEmailnput}
                Save
              {:else}
                Change email
              {/if}
            </button>
          </div>
        </formset>

        <formset class="password">
          <h3>Password:</h3>
          <div class="user">
            {#if showPasswordInput}
              <formset class="change-password">
                <label>
                  New Password
                  <input type="password" bind:value={password} />
                </label>
                <label>
                  Confirm New Password
                  <input type="password" bind:value={passwordConfirmation} />
                </label>
              </formset>
            {:else if busy}
              <i>Cannot change password for anonymous user</i>
            {:else}
              <p>************</p>
            {/if}
            <button
              class="large floaty inverted"
              type="submit"
              on:click={passwordButtonPressed}
              disabled={showPasswordInput ? !confirmedPassword : busy}
            >
              {#if showPasswordInput}
                Save
              {:else}
                Change password
              {/if}
            </button>
          </div>
        </formset>
      {/if}
    </form>
  </section>
</WhitePage>

<style lang="scss">
  p.loading {
    text-align: center;
  }

  header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  section {
    display: flex;
    flex-direction: column;
    align-items: baseline;
  }

  form {
    width: 100%;
    padding: 1rem;
    border: 1px solid var(--primary);
    border-radius: 15px;

    display: flex;
    flex-direction: column;
    gap: 1rem;

    h3 {
      margin: 1rem 0;
    }

    div.user {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    label {
      display: flex;
      flex-direction: column;
    }

    formset.avatar {
      input[type="file"] {
        height: 100%;
        margin: 0;
      }

      div[role="group"] {
        display: flex;

        & > *:not(:first-child) {
          border-radius: 0 15px 15px 0;
        }

        & > *:not(:last-child) {
          border-radius: 15px 0 0 15px;
        }

        button {
          width: fit-content;
        }
      }
    }

    input {
      margin-top: 0.25em;
      padding: 0.5em;
      border: 1px solid var(--primary);
      border-radius: 15px;
    }

    formset.change-password {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
  }

  img.avatar {
    border-radius: 50%;
    width: 120px;
    margin-right: 20px;
    border: 2px solid var(--primary);
  }
</style>
