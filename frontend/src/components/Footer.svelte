<footer class="bg-neutral-950 text-white pt-14 pb-8">
  <div class="flex flex-col lg:flex-row items-center justify-between">
    <div class="flex flex-col items-center lg:items-start">
      <img src="/logo.png" alt="Logo" class="w-32 pl-4" />
    </div>

    <nav class="flex flex-col lg:flex-row lg:space-x-4">
      <div>
        <a href="/">Product</a>
        <a href="/blog/research">Research</a>
        <a href="/blog/news">News</a>
      </div>
      <div>
        <a href="/careers">Careers</a>
        <a href="https://ko-fi.com/ameerarsala", target="_blank">Support Us</a>
        <a href="https://github.com/AmeerArsala/UniverseLM" target="_blank">GitHub</a>
        <a href="https://www.linkedin.com/in/ameer-arsala/" target="_blank"
          >LinkedIn</a
        >
      </div>
      <div>
        <a href="#">Terms of Service</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Acceptable Use Policy</a>
      </div>
    </nav>

    <div class="mt-8 pr-6 text-right text-neutral-600">
      <p>&copy; UniverseLM</p>
    </div>
  </div>
</footer>

<style>
  footer {
    text-align: center;
  }

  footer img {
    max-width: 100%;
  }

  footer nav {
    flex-grow: 1;
    text-align: center;
  }

  footer a {
    color: #fff;
    text-decoration: none;
    display: block;
    margin-bottom: 15px;
  }

  footer a:hover {
    text-decoration: underline;
  }

  @media (min-width: 768px) {
    footer nav {
      display: flex;
    }

    footer div {
      flex: 1;
    }
  }
</style>
