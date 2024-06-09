/**
 * <COMMAND OPTIONS>
 *
 * SUGGESTIONS
 * ...
 *
 * PLATFORM
 * Home
 * Create Community
 * Explore Communities
 *
 * SETTINGS
 * Profile
 * Generate API Key
 * Billing
 *
 * INTERFACES
 * API
 * CLI
 * Discord Bot
 * Slack Bot
 *
 * WIKI
 * Docs
 * Blog: posts
 * Blog: research
 * Blog: news
 * Source
 *
 */

import { createCommunityOpen, generateAPIKeyOpen } from "@components/Dashboard/dashboardStores";
import { hasAPIKey } from "$lib/data/datafunctions";

import {
  IconHome,           // Dashboard home
  IconTopologyRing,   // Explore Communities
  IconSquarePlus,     // Create community
  IconFileLambda,     // Docs
  IconWallet,         // Billing
  IconUser,           // Profile

  IconKey,
  IconApi,
  IconTerminal2,
  IconArticle,
  IconBrain,
  IconNews,
  IconBrandDiscord,
  IconBrandSlack,
  IconBrandGithub,
} from '@tabler/icons-react';

import { Button } from '@components/ui/react-button/button';
import {
	CommandDialog,
	CommandEmpty,
	CommandGroup,
	CommandInput,
	CommandItem,
	CommandList,
	CommandSeparator,
	CommandShortcut,
} from '@components/ui/react-command/Command';
import { cn } from '$lib/utils';
import {
	CalendarIcon,
	EnvelopeClosedIcon,
	FaceIcon,
	GearIcon,
	PersonIcon,
	RocketIcon,
} from '@radix-ui/react-icons';
import { Laptop, Moon, Sun } from 'lucide-react';
import * as React from 'react';

function removeItem(arr: any[], idx: number) {
  return arr.splice(idx, 1)[0];
}

export function CommandMenu() {
  const [open, setOpen] = React.useState(false);

	React.useEffect(() => {
		const down = (e: KeyboardEvent) => {
			if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
				e.preventDefault();
				setOpen((open) => !open);
			}
		};

		document.addEventListener('keydown', down);
		return () => document.removeEventListener('keydown', down);
	}, []);

  // Event handling for closing with ESC
  React.useEffect(() => {
		const down = (e: KeyboardEvent) => {
			if (e.key === 'esc' && open) {
				e.preventDefault();
				setOpen((open) => false);
			}
		};

		document.addEventListener('keydown', down);
		return () => document.removeEventListener('keydown', down);
	}, []);

  const platformGroup: any[] = [
    /**
     * Home
     * Create Community
     * Explore Communities
     */
    (
      <CommandItem onSelect={() => { window.location.href = "/platform"; }}>
        <IconHome className="mr-2 h-4 w-4" />
        <span>Home</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { setOpen((open) => false); createCommunityOpen.set(true); }}>
        <IconSquarePlus className="mr-2 h-4 w-4" />
        <span>Create Community</span>
        <CommandShortcut>⌘.</CommandShortcut>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/platform/explore"; }}>
        <IconTopologyRing className="mr-2 h-4 w-4" />
        <span>Explore Communities</span>
      </CommandItem>
    )
  ];

  const settingsGroup: any[] = [
    /**
     * Profile
     * Generate API Key
     * Billing
     */
    (
      <CommandItem onSelect={() => { window.location.href = "/platform/profile"; }}>
        <IconUser className="mr-2 h-4 w-4" />
        <span>Profile</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { setOpen((open) => false); generateAPIKeyOpen.set(true); }}>
        <IconKey className="mr-2 h-4 w-4" />
        <span>Generate API Key</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/platform/billing"; }}>
        <IconWallet className="mr-2 h-4 w-4" />
        <span>Billing</span>
      </CommandItem>
    )
  ];

  const interfacesGroup: any[] = [
    /**
     * API
     * CLI
     * Discord Bot
     * Slack Bot
     */
    (
      <CommandItem onSelect={() => { window.location.href = "/api"; }}>
        <IconApi className="mr-2 h-4 w-4" />
        <span>API</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/cli"; }}>
        <IconTerminal2 className="mr-2 h-4 w-4" />
        <span>CLI</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/integrations/discord"; }}>
        <IconBrandDiscord className="mr-2 h-4 w-4" />
        <span>Discord Bot</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/integrations/slack"; }}>
        <IconBrandSlack className="mr-2 h-4 w-4" />
        <span>Slack Bot</span>
      </CommandItem>
    )
  ];

  const wikiGroup: any[] = [
    /**
     * Docs
     * Blog: posts
     * Blog: research
     * Blog: news
     * Source
     */
    (
      <CommandItem onSelect={() => { window.location.href = "/platform/docs"; }}>
        <IconFileLambda className="mr-2 h-4 w-4" />
        <span>Docs</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/blog/posts"; }}>
        <IconArticle className="mr-2 h-4 w-4" />
        <span>Blog Posts</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/blog/research"; }}>
        <IconBrain className="mr-2 h-4 w-4" />
        <span>Research</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "/blog/news"; }}>
        <IconNews className="mr-2 h-4 w-4" />
        <span>News</span>
      </CommandItem>
    ),
    (
      <CommandItem onSelect={() => { window.location.href = "https://github.com/AmeerArsala/UniverseLM"; }}>
        <IconBrandGithub className="mr-2 h-4 w-4" />
        <span>Source</span>
      </CommandItem>
    )
  ];

  const suggestedGroup: any[] = [];

  if (!hasAPIKey()) {
    const GENERATE_API_KEY_IDX = 1;
    suggestedGroup.push(removeItem(settingsGroup, GENERATE_API_KEY_IDX));
  }

	return (
		<>
			<Button
				variant="outline"
				className={cn(
					'relative h-8 w-full justify-start rounded-[0.5rem] bg-background text-sm font-normal text-muted-foreground shadow-none sm:pr-12 md:w-40 lg:w-64 mb-5',
				)}
				onClick={() => setOpen((open) => !open)}
			>
				<span className="inline-flex">Search...</span>
				<kbd className="pointer-events-none absolute right-[0.3rem] top-[0.3rem] hidden h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
					<span className="text-xs">⌘</span>K
				</kbd>
			</Button>
			<CommandDialog open={open} onOpenChange={setOpen}>
				<CommandInput placeholder="Type a command or search..." />
				<CommandList>
					<CommandEmpty>No results found.</CommandEmpty>

					{suggestedGroup.length > 0 && (
            <CommandGroup heading="Suggestions">
              {suggestedGroup}
            </CommandGroup>
          )}

          <CommandSeparator />

          <CommandGroup heading="Platform">
						{platformGroup}
					</CommandGroup>

          <CommandGroup heading="Settings">
						{settingsGroup}
					</CommandGroup>

          <CommandGroup heading="Interfaces">
						{interfacesGroup}
					</CommandGroup>

          <CommandGroup heading="Wiki">
						{wikiGroup}
					</CommandGroup>

					<CommandGroup heading="Theme">
						<CommandItem onSelect={() => setTheme('light')}>
							<Sun className="mr-2 h-4 w-4" />
							Change theme to light
						</CommandItem>
						<CommandItem onSelect={() => setTheme('dark')}>
							<Moon className="mr-2 h-4 w-4" />
							Change theme to dark
						</CommandItem>
						<CommandItem onSelect={() => setTheme('system')}>
							<Laptop className="mr-2 h-4 w-4" />
							Change theme to system
						</CommandItem>
					</CommandGroup>
				</CommandList>
			</CommandDialog>
		</>
	);

	type Theme = 'light' | 'dark' | 'system';

	function setTheme(theme: Theme) {
		localStorage.setItem('theme', theme);
		const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
			? 'dark'
			: 'light';

		const newTheme = theme === 'system' ? systemTheme : theme;

		document.documentElement.classList.remove('light', 'dark');
		document.documentElement.classList.add(newTheme);
		setOpen((open) => !open);
	}
}
