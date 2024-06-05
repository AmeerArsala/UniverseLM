<script lang='ts'>
  import { onMount } from "svelte";
  import { githubStars } from "$lib/data/stores";
  import { updateStargazers } from "$lib/scripts/updatestate";

  export let repo_link: string = "https://github.com/AmeerArsala";
  export let stars: number = isNaN(githubStars.getNum()) ? 0 : githubStars.getNum();
  export let manual: boolean = false;
  export let autoUpdateStars: boolean = false;

  onMount(async () => {
    if (manual) {
      // It was purposefully set--Don't touch it
      console.log("not touching the stargazers");
      return;
    } else {
      console.log("stargazers (initial): " + stars);
      githubStars.getAtom().subscribe((value, oldValue) => {
        stars = parseInt(value);
      });
    }

    if (autoUpdateStars) {
      // actually calculate it
      stars = await updateStargazers(repo_link);
      // stars = githubStars.getNum();  // will update anyway so I commented this out
    }
  });

  /*if (stars === -1) {
    // it was not set
    stars = 7984;
  }*/
</script>

<a class="repo-element" href={repo_link} target="_blank">
  <div class="px-3 relative">
    <div class="absolute inset-y-0.5 inset-x-1.5 bg-gray-800 rounded-md" />
    <div class="relative flex items-center space-x-0 text-gray-800">
      <!--GITHUB ICON-->
      <svg class="social-media-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
        <defs>
          <linearGradient id="pop-gradient">
            <stop offset="0%" style="stop-color:rgb(99, 102, 241); stop-opacity:1"/>
            <stop offset="100%" style="stop-color:rgb(139, 92, 246); stop-opacity:1"/>
          </linearGradient>
        </defs>

        <!--GitHub Icon-->
        <path class="github-icon" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" fill="#ffff"/>
      </svg>

      <!--STAR COUNT-->
      <div class="px-4 relative">
        <div class="absolute inset-y-0 inset-x-0 bg-gray-600 rounded-md" />
        <span class="relative flex text-medium font-medium text-white">{stars}</span>
      </div>
    </div>
  </div>
</a>

<style>
  .social-media-icon {
		width: 1.5rem;
		height: 1.5rem;
		margin: 0.5rem;
		object-fit: contain;
	}

  :where(.repo-element:hover) .github-icon {
    transition-duration: 200ms;
    fill: url(#pop-gradient);
  }
</style>
