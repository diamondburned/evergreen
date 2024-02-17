<div class="container background">
  <div class="content">
    <slot />
  </div>
  <img src="/blurred.webp" alt="Blurry background" />
</div>

<style lang="scss">
  .container {
    display: flex;
    justify-content: center;
    align-items: center;

    position: relative;
    width: 100%;
    height: 100%;

    img {
      --margin: 50px;

      position: absolute;
      width: calc(100% - var(--margin) * 2);
      height: calc(100% - var(--margin) * 2);

      border-radius: 25px;
      outline: 1.5px solid;
      box-shadow: 4em 4em 0.5em 0.5em var(--md-sys-color-shadow) inset;

      z-index: 0;
    }

    .content {
      z-index: 1;
    }
  }
</style>
