<script lang="ts">
  let thing = "hi";
</script>

<svelte:head>
  <title>Home</title>
  <meta name="description" content="Svelte demo app" />
</svelte:head>

<div class="container background">
  <img src="/blurred.webp"/>
  <h1>Evergreen</h1>
  <button><p class="on-secondary-text">Play</p></button>
  <h3>Already played? <u>Login</u></h3>
</div>

<style lang="scss">
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 800px;
    img {
      width:95%;
      height:90%;
      border-radius:25px;
      border: 1px solid;
      box-shadow: 4em 4em 0.5em 0.5em var(--md-sys-color-shadow) inset;
    }
    h1 {
      position: absolute;
      top: 320px;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 60px;
      text-shadow: 2px 2px 2px black;
    }
    button {
      margin-top: 90px;
      position: absolute;
      width: 200px;
      height: 45px;
      border-radius: 15px;
      transition: all 0.15s linear;
      p {
        font-size: 22px;
        margin: auto;
      }
    }
    button:hover {
      box-shadow: 0 0.5em 0.5em -0.4em var(--md-sys-color-shadow);
    }

    h3 {
      margin-top: 240px;
      position: absolute;
    }
  }
</style>