import { CardDescription, CardHeader, CardTitle } from "@components/ui/react-card/card";

import { useStore } from "@nanostores/react";
import { isYearly } from "./pricingStore";

import { cn } from "$lib/utils";

export interface PricingCardHeaderProps {
  title: string;
  monthlyPrice?: number;
  yearlyPrice?: number;
  description: string;
  popular?: boolean;
}

export default function PricingCardHeader(props: PricingCardHeaderProps) {
  const { title, monthlyPrice, yearlyPrice, description, popular } = props;
  const $isYearly = useStore(isYearly);

  // For year plan, you save money if you choose it over simply paying monthly for 12 months
  const yearlySavings = Math.round((monthlyPrice * 12 - yearlyPrice) * 100) / 100;
  const yearlySavingsPercent = Math.round((yearlySavings / yearlyPrice) * 100);

  const priceMonthly: string = monthlyPrice ? monthlyPrice.toFixed(2) : "TBD";
  const priceYearly: string = yearlyPrice ? yearlyPrice.toFixed(2) : "TBD";

  return (
    <CardHeader className="pb-8 pt-4">
      {$isYearly && yearlyPrice && monthlyPrice && monthlyPrice >= 0.01 ? (
        <div className="flex justify-between">
          <CardTitle className="text-zinc-700 dark:text-zinc-300 text-lg">{title}</CardTitle>
          <div
            className={cn("px-2.5 rounded-xl h-fit text-sm py-1 bg-zinc-200 text-black dark:bg-zinc-800 dark:text-white", {
              "bg-gradient-to-r from-orange-400 to-rose-400 dark:text-black ": popular,
            })}>
            Save {yearlySavingsPercent}%
          </div>
        </div>
      ) : (
        <CardTitle className="text-zinc-700 dark:text-zinc-300 text-lg">{title}</CardTitle>
      )}
      <div className="flex gap-0.5">
        <h3 className="text-3xl font-bold">{yearlyPrice && $isYearly ? ("$" + priceYearly) : monthlyPrice ? ("$" + priceMonthly) : "Custom"}</h3>
        <span className="flex flex-col justify-end text-sm mb-1">{yearlyPrice && $isYearly ? "/year" : monthlyPrice ? "/month" : null}</span>
      </div>
      <CardDescription className="pt-1.5 h-12">{description}</CardDescription>
    </CardHeader>
  );
}
