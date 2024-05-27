
<script lang="ts">
  import * as RadioGroup from "$lib/components/ui/radio-group/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import SignUpDialog from '@components/AuthForms/SignUpDialog.svelte';

  interface PricingTierFrequency {
    id: string;
    value: string;
    label: string;
    priceSuffix: string;
  }

  interface PricingTier {
    name: string;
    id: string;
    href: string | Record<string, string>;
    discountPrice: string | Record<string, string>;
    price: string | Record<string, string>;
    description: string | React.ReactNode;
    features: string[];
    featured?: boolean;
    highlighted?: boolean;
    cta: string;
    soldOut?: boolean;
  }

  export const frequencies: PricingTierFrequency[] = [
    { id: '1', value: '1', label: 'Monthly', priceSuffix: '/month' },
    { id: '2', value: '2', label: 'Annually', priceSuffix: '/year' },
  ];

  const PRO_SUBSCRIPTION = {
    monthlyLink: "https://buy.stripe.com/5kA02Qfkl73HeZy4gg",
    yearlyLink: "https://buy.stripe.com/14k2aY8VXew9bNm5kl"
  }

  export const tiers: PricingTier[] = [
    {
      name: 'Free',
      id: '0',
      href: '/subscribe',
      price: { '1': '$0', '2': '$0' },
      discountPrice: { '1': '', '2': '' },
      description: `Get all goodies for free, no credit card required.`,
      features: [
        `Create 5 communities`,
        `Limited free queries`
      ],
      featured: false,
      highlighted: false,
      soldOut: false,
      cta: `Sign up`,
    },
    {
      name: 'Pro',
      id: '1',
      href: {'1': PRO_SUBSCRIPTION.monthlyLink, '2': PRO_SUBSCRIPTION.yearlyLink},
      price: { '1': '$3.99', '2': '$39.99' },
      discountPrice: { '1': '', '2': '' },
      description: `For those who love this product! Get more now!`,
      features: [
        `All in the free plan plus`,
        `Nearly Unlimited Communities`,
        `Nearly Unlimited Queries`,
        `Integration with third-party apps`,
      ],
      featured: false,
      highlighted: true,
      soldOut: false,
      cta: `Get started`,
    },
    {
      name: 'Scale',
      id: '2',
      href: '/contact-us',
      price: { '1': 'TBD', '2': 'TBD' },
      discountPrice: { '1': '', '2': '' },
      description: `When you need scale, you need more power and flexibility.`,
      features: [
        `All in the pro plan plus`,
        `Priority support`,
        `Enterprise-grade security`,
      ],
      featured: true,
      highlighted: false,
      soldOut: false,
      cta: `Contact Us`,
    },
  ];

  const cn = (...args: Array<string | boolean | undefined | null>) =>
    args.filter(Boolean).join(' ');

  let frequency = frequencies[0];

  const bannerText = '';

  let freetier = tiers[0];
  let protier = tiers[1];
  let scaletier = tiers[2];
</script>

<div
  class={cn('flex flex-col w-full items-center fancyOverlay')}
>
  <div class="w-full flex flex-col items-center">
    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex flex-col items-center">
      <div class="w-full lg:w-auto mx-auto max-w-4xl lg:text-center">
        <h1 class="text-black dark:text-white text-4xl font-semibold font-pjsans max-w-xs sm:max-w-none md:text-6xl !leading-tight">
          Pricing
        </h1>

      </div>

      {#if bannerText}
        <div class="w-full lg:w-auto flex justify-center my-4">
          <p class="w-full px-4 py-3 text-xs bg-sky-100 text-black dark:bg-sky-300/30 dark:text-white/80 rounded-xl">
            {bannerText}
          </p>
        </div>
      {/if}

      {#if frequencies.length > 1}
        <div class="mt-16 flex justify-center">
          <RadioGroup.Root
            value={frequency.value}
            class="grid gap-x-1 rounded-full p-1 text-center text-xs font-semibold leading-5 bg-white dark:bg-black ring-1 ring-inset ring-gray-200/30 dark:ring-gray-800"
            style={`grid-template-columns: repeat(${frequencies.length}, minmax(0, 1fr));`}
          >
            <Label class="sr-only">Payment frequency</Label>
            {#each frequencies as option}
              <Label
                class={cn(
                  frequency.value === option.value
                    ? 'bg-sky-500/90 text-white dark:bg-sky-900/70 dark:text-white/70'
                    : 'bg-transparent text-gray-500 hover:bg-sky-500/10',
                  'cursor-pointer rounded-full px-2.5 py-2 transition-all',
                )}
                for={option.value}
              >
                {option.label}

                <RadioGroup.Item
                  value={option.value}
                  id={option.value}
                  class="hidden"
                  on:click={() => { frequency = option; }}
                />
              </Label>
            {/each}
          </RadioGroup.Root>
        </div>
      {:else}
        <div class="mt-12" aria-hidden="true"></div>
      {/if}

      <div
      class={cn(
        'isolate mx-auto mt-4 mb-28 grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none select-none',
        tiers.length === 2 ? 'lg:grid-cols-2' : '',
        tiers.length === 3 ? 'lg:grid-cols-3' : '',
      )}
    >
        <!--FREE-->
        <div
          class={cn(
            freetier.featured
              ? '!bg-gray-900 ring-gray-900 dark:!bg-gray-100 dark:ring-gray-100'
              : 'bg-white dark:bg-gray-900/80 ring-gray-300/70 dark:ring-gray-700',
            'max-w-xs ring-1 rounded-3xl p-8 xl:p-10',
            freetier.highlighted ? "fancyGlassContrast" : '',
          )}
        >
          <h3
            id={freetier.id}
            class={cn(
              freetier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
              'text-2xl font-bold tracking-tight',
            )}
          >
            {freetier.name}
          </h3>
          <p
            class={cn(
              freetier.featured
                ? 'text-gray-300 dark:text-gray-500'
                : 'text-gray-600 dark:text-gray-400',
              'mt-4 text-sm leading-6',
            )}
          >
            {freetier.description}
          </p>
          <p class="mt-6 flex items-baseline gap-x-1">
            <span
              class={cn(
                freetier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
                'text-4xl font-bold tracking-tight',
                  freetier.discountPrice &&
                    freetier.discountPrice[ frequency.value ]
                  ? 'line-through'
                  : '',
              )}
            >
              {typeof freetier.price === 'string'
                ? freetier.price
                : freetier.price[frequency.value]}
            </span>

            <span
              class={cn(
                freetier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
              )}
            >
              {typeof freetier.discountPrice === 'string'
                ? freetier.discountPrice
                : freetier.discountPrice[frequency.value]}
            </span>

            {#if typeof freetier.price !== 'string'}
              <span
                class={cn(
                  freetier.featured
                    ? 'text-gray-300 dark:text-gray-500'
                    : 'dark:text-gray-400 text-gray-600',
                  'text-sm font-semibold leading-6',
                )}
              >
                {frequency.priceSuffix}
              </span>
            {/if}
          </p>
          <Dialog.Root>
            <Dialog.Trigger>
              <div
                aria-describedby={freetier.id}
                class={cn(
                  'flex mt-6 shadow-sm',
                  freetier.soldOut ? 'pointer-events-none' : '',
                )}
              >
                <button
                  disabled={freetier.soldOut}
                  class={cn(
                    'w-full inline-flex items-center justify-center font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 text-black dark:text-white hover:opacity-80 dark:border-0 h-12 rounded-md px-6 sm:px-10 text-md',
                    freetier.featured || freetier.soldOut ? 'grayscale' : '',
                    !freetier.highlighted && !freetier.featured
                      ? 'bg-gray-100 dark:bg-gray-600 border border-solid border-gray-300 dark:border-gray-800'
                      : 'bg-sky-300/70 text-sky-foreground hover:bg-sky-400/70 dark:bg-sky-700 dark:hover:bg-sky-800/90',
                    freetier.featured ? '!bg-gray-100 dark:!bg-black' : '',
                  )}
                >
                  {freetier.soldOut ? 'Sold out' : freetier.cta}
                </button>
              </div>
            </Dialog.Trigger>

            <!--TODO: Make this only happen if not signed in-->
            <SignUpDialog/>
          </Dialog.Root>

          <ul
            class={cn(
              freetier.featured
                ? 'text-gray-300 dark:text-gray-500'
                : 'text-gray-700 dark:text-gray-400',
              'mt-8 space-y-3 text-sm leading-6 xl:mt-10',
            )}
          >
            {#each freetier.features as feature}
              <li class="flex gap-x-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class={cn('w-6 h-6', freetier.featured ? 'text-white dark:text-black' : '',
                    freetier.highlighted
                      ? 'text-sky-500'
                      : 'text-gray-500',

                    'h-6 w-5 flex-none',)}
                >
                  <path
                    fill-rule="evenodd"
                    d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
                    clip-rule="evenodd"
                  />
                </svg>
                {feature}
              </li>
            {/each}
          </ul>
        </div>

        <!--PRO TIER-->
        <div
          class={cn(
            protier.featured
              ? '!bg-gray-900 ring-gray-900 dark:!bg-gray-100 dark:ring-gray-100'
              : 'bg-white dark:bg-gray-900/80 ring-gray-300/70 dark:ring-gray-700',
            'max-w-xs ring-1 rounded-3xl p-8 xl:p-10',
            protier.highlighted ? "fancyGlassContrast" : '',
          )}
        >
          <h3
            id={protier.id}
            class={cn(
              protier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
              'text-2xl font-bold tracking-tight',
            )}
          >
            {protier.name}
          </h3>
          <p
            class={cn(
              protier.featured
                ? 'text-gray-300 dark:text-gray-500'
                : 'text-gray-600 dark:text-gray-400',
              'mt-4 text-sm leading-6',
            )}
          >
            {protier.description}
          </p>
          <p class="mt-6 flex items-baseline gap-x-1">
            <span
              class={cn(
                protier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
                'text-4xl font-bold tracking-tight',
                  protier.discountPrice &&
                    protier.discountPrice[
                      frequency.value
                    ]
                  ? 'line-through'
                  : '',
              )}
            >
              {typeof protier.price === 'string'
                ? protier.price
                : protier.price[frequency.value]}
            </span>

            <span
              class={cn(
                protier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
              )}
            >
              {typeof protier.discountPrice === 'string'
                ? protier.discountPrice
                : protier.discountPrice[frequency.value]}
            </span>

            {#if typeof protier.price !== 'string'}
              <span
                class={cn(
                  protier.featured
                    ? 'text-gray-300 dark:text-gray-500'
                    : 'dark:text-gray-400 text-gray-600',
                  'text-sm font-semibold leading-6',
                )}
              >
                {frequency.priceSuffix}
              </span>
            {/if}
          </p>

          <a
            href={protier.href[protier.id]}
            aria-describedby={protier.id}
            class={cn(
              'flex mt-6 shadow-sm',
              protier.soldOut ? 'pointer-events-none' : '',
            )}
          >
            <button
              disabled={protier.soldOut}
              class={cn(
                'w-full inline-flex items-center justify-center font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 text-black dark:text-white hover:opacity-80 dark:border-0 h-12 rounded-md px-6 sm:px-10 text-md',
                protier.featured || protier.soldOut ? 'grayscale' : '',
                !protier.highlighted && !protier.featured
                  ? 'bg-gray-100 dark:bg-gray-600 border border-solid border-gray-300 dark:border-gray-800'
                  : 'bg-sky-300/70 text-sky-foreground hover:bg-sky-400/70 dark:bg-sky-700 dark:hover:bg-sky-800/90',
                protier.featured ? '!bg-gray-100 dark:!bg-black' : '',
              )}
            >
              {protier.soldOut ? 'Sold out' : protier.cta}
            </button>
          </a>

          <ul
            class={cn(
              protier.featured
                ? 'text-gray-300 dark:text-gray-500'
                : 'text-gray-700 dark:text-gray-400',
              'mt-8 space-y-3 text-sm leading-6 xl:mt-10',
            )}
          >
            {#each protier.features as feature}
              <li class="flex gap-x-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class={cn('w-6 h-6', freetier.featured ? 'text-white dark:text-black' : '',
                    freetier.highlighted
                      ? 'text-sky-500'
                      : 'text-gray-500',

                    'h-6 w-5 flex-none',)}
                >
                  <path
                    fill-rule="evenodd"
                    d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
                    clip-rule="evenodd"
                  />
                </svg>
                {feature}
              </li>
            {/each}
          </ul>
        </div>

      <!--SCALE TIER-->
        <div
          class={cn(
            scaletier.featured
              ? '!bg-gray-900 ring-gray-900 dark:!bg-gray-100 dark:ring-gray-100'
              : 'bg-white dark:bg-gray-900/80 ring-gray-300/70 dark:ring-gray-700',
            'max-w-xs ring-1 rounded-3xl p-8 xl:p-10',
            scaletier.highlighted ? "fancyGlassContrast" : '',
          )}
        >
          <h3
            id={scaletier.id}
            class={cn(
              scaletier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
              'text-2xl font-bold tracking-tight',
            )}
          >
            {scaletier.name}
          </h3>
          <p
            class={cn(
              scaletier.featured
                ? 'text-gray-300 dark:text-gray-500'
                : 'text-gray-600 dark:text-gray-400',
              'mt-4 text-sm leading-6',
            )}
          >
            {scaletier.description}
          </p>
          <p class="mt-6 flex items-baseline gap-x-1">
            <span
              class={cn(
                scaletier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
                'text-4xl font-bold tracking-tight',
                  scaletier.discountPrice &&
                    scaletier.discountPrice[
                      frequency.value
                    ]
                  ? 'line-through'
                  : '',
              )}
            >
              {typeof scaletier.price === 'string'
                ? scaletier.price
                : scaletier.price[frequency.value]}
            </span>

            <span
              class={cn(
                scaletier.featured ? 'text-white dark:text-black' : 'text-black dark:text-white',
              )}
            >
              {typeof scaletier.discountPrice === 'string'
                ? scaletier.discountPrice
                : scaletier.discountPrice[frequency.value]}
            </span>

            {#if typeof scaletier.price !== 'string'}
              <span
                class={cn(
                  scaletier.featured
                    ? 'text-gray-300 dark:text-gray-500'
                    : 'dark:text-gray-400 text-gray-600',
                  'text-sm font-semibold leading-6',
                )}
              >
                {frequency.priceSuffix}
              </span>
            {/if}
          </p>
          <a
            href={scaletier.href.toString()}
            aria-describedby={scaletier.id}
            class={cn(
              'flex mt-6 shadow-sm',
              scaletier.soldOut ? 'pointer-events-none' : '',
            )}
          >
            <button
              disabled={scaletier.soldOut}
              class={cn(
                'w-full inline-flex items-center justify-center font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 text-black dark:text-white hover:opacity-80 dark:border-0 h-12 rounded-md px-6 sm:px-10 text-md',
                scaletier.featured || scaletier.soldOut ? 'grayscale' : '',
                !scaletier.highlighted && !scaletier.featured
                  ? 'bg-gray-100 dark:bg-gray-600 border border-solid border-gray-300 dark:border-gray-800'
                  : 'bg-sky-300/70 text-sky-foreground hover:bg-sky-400/70 dark:bg-sky-700 dark:hover:bg-sky-800/90',
                scaletier.featured ? '!bg-gray-100 dark:!bg-black' : '',
              )}
            >
              {scaletier.soldOut ? 'Sold out' : scaletier.cta}
            </button>
          </a>

          <ul
            class={cn(
              scaletier.featured
                ? 'text-gray-300 dark:text-gray-500'
                : 'text-gray-700 dark:text-gray-400',
              'mt-8 space-y-3 text-sm leading-6 xl:mt-10',
            )}
          >
            {#each scaletier.features as feature}
              <li class="flex gap-x-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class={cn('w-6 h-6', freetier.featured ? 'text-white dark:text-black' : '',
                    freetier.highlighted
                      ? 'text-sky-500'
                      : 'text-gray-500',

                    'h-6 w-5 flex-none',)}
                >
                  <path
                    fill-rule="evenodd"
                    d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
                    clip-rule="evenodd"
                  />
                </svg>
                {feature}
              </li>
            {/each}
          </ul>
        </div>

      </div>
    </div>
  </div>
</div>

<style>
  .fancyOverlay,
  .fancyGlass {
    --primary-light: theme('colors.sky.400');
    --primary-main: #6366f1;
    --primary-darker: #a855f7;
    --secondary-light: theme('colors.indigo.400');
    --secondary-main: #6366f1;
    --secondary-darker: #a855f7;
    --glass-color: 99, 102, 241;
  }

  /**
    * Overlay gradients & animation - used as page background.
    */
  @property --fancy-x {
    syntax: '<percentage>';
    inherits: true;
    initial-value: 0%;
  }
  @property --fancy-y {
    syntax: '<percentage>';
    inherits: true;
    initial-value: 0%;
  }

  @keyframes roundabout {
    0% {
      --fancy-x: 60%;
      --fancy-y: 20%;

      opacity: 0;
    }

    5% {
      --fancy-x: 80%;
      --fancy-y: 10%;
    }

    20% {
      --fancy-x: 95%;
      --fancy-y: 5%;

      opacity: var(--maximum-opacity);
    }

    100% {
      --fancy-x: 100%;
      --fancy-y: 0%;

      opacity: var(--maximum-opacity);
    }
  }
  /**
    * Glass effect with a gradient background and blur - used for highlighting pricing cards.
    */
  .fancyGlass,
  .fancyGlassContrast {
    background: radial-gradient(
        63.94% 63.94% at 50% 0%,
        rgba(var(--glass-color), 0.12) 0%,
        rgba(var(--glass-color), 0) 100%
      ),
      rgba(var(--glass-color), 0.01);
    backdrop-filter: blur(6px);
    position: relative;
    overflow: hidden;
  }

  .fancyGlassContrast:after {
    content: '';
    width: calc(100% + 2px);
    height: calc(100% + 2px);
    background: var(--primary-darker);
    opacity: 0.1;
    position: absolute;
    top: -1px;
    left: -1px;
    z-index: -1;
  }

  .fancyGlassContrast:before,
  .fancyGlass:before {
    content: '';
    width: calc(100% + 2px);
    height: calc(100% + 2px);
    background: linear-gradient(
        rgba(var(--glass-color), 0.12) 0%,
        rgba(var(--glass-color), 0) 74.04%
      ),
      linear-gradient(
        0deg,
        rgba(var(--glass-color), 0.04),
        rgba(var(--glass-color), 0.04)
      );
    position: absolute;
    top: -1px;
    left: -1px;
    mask: url("data:image/svg+xml,%3Csvg width='402' height='202' viewBox='0 0 402 202' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='0.5' y='0.5' width='401' height='201' rx='9.5' /%3E%3C/svg%3E%0A");
    pointer-events: none;
  }
</style>
