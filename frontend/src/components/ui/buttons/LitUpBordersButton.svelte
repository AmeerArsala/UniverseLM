<script>
  export let text = "Lit up borders";
</script>

<button class="p-[3px] relative">
  <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
  <div class="px-8 py-2  bg-black rounded-[6px] relative group text-white transition duration-200 hover:bg-transparent">
    {text}
  </div>
</button>
