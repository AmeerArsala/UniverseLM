import { Tabs, TabsList, TabsTrigger } from "@components/ui/react-tabs/tabs";

import { useStore } from "@nanostores/react";
import { isYearly } from "./pricingStore";


export default function PricingSwitch() {
  const $isYearly = useStore(isYearly);

  return (
    <Tabs defaultValue="0" className="w-40 mx-auto" onValueChange={(value: string) => isYearly.set(!$isYearly)}>
      <TabsList className="py-6 px-2">
        <TabsTrigger value="0" className="text-base">
          Monthly
        </TabsTrigger>
        <TabsTrigger value="1" className="text-base">
          Yearly
        </TabsTrigger>
      </TabsList>
    </Tabs>
  );
}
