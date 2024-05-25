"use client";

import { PlaceholdersAndVanishInput } from "@components/ui/placeholders-and-vanish-input";

export function SocietyGenerator() {
  const placeholders = [
    "the wild west",
    "a fantastical kingdom",
    "a 2000s sitcom",
    "Ancient Greece",
    "a melodramatic war setting",
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("submitted");
  };
  return (
    <div className="h-[15rem] flex flex-col justify-center  items-center px-4">
      <h2 className="mb-5 sm:mb-10 text-xl text-center sm:text-5xl dark:text-white text-black">
        Generate a Society
      </h2>
      <PlaceholdersAndVanishInput
        placeholders={placeholders}
        onChange={handleChange}
        onSubmit={onSubmit}
      />
    </div>
  );
}
