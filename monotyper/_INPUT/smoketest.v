(*@file@*)
(*@H.1@[[Proofcase / T000 / CIC Integration]]@*)
(*@H.2@[[Overview]]@*)
(*@p.l@[[This file is the top-level CIC route for T000. It binds the package-local CIC folder into one stable import point for downstream surfaces.]]@*)
(*@p.l@[[The current CIC payload is the pigeonhole divisibility development]]@*)
(*@plist.arabic@[[`R01__Odd_Part`]][[`R02__Pigeonhole_Divisibility`]]@*)
(*@p.l@[[Architecturally, `R01__CIC` is the integration layer of the package. The abstract combinatorial contribution belongs to `R02__Pigeonhole_Divisibility`, whose role is to provide the generallist-pigeonhole mechanism in a form independent of the final arithmetic application. The present file performs the closing specialization: it combines that abstract machinery with the odd-part codomain control and divisibility bridge supplied by `R01__Odd_Part`, and thereby derives the package-level endpoint `pigeonhole_divisibility_CIC`.]]@*)
From Coq Require Import Arith Lia List PeanoNat.

From T000.CIC__Pigeonhole_Divisibility Require Export
  R01__Odd_Part
  R02__Pigeonhole_Divisibility.
(*@c.standard@[[Top-level CIC endpoint. We restate the final divisibility theorem at the package boundary by combining the abstract pigeonhole route with the odd-part arithmetic route.]]@*)
Theorem pigeonhole_divisibility_CIC :
  forall n A,
    (forall a, In a A -> 1 <= a /\ a <= 2 * n) ->
    NoDup A ->
    length A = n + 1 ->
    exists a b,
      In a A /\
      In b A /\
      a <> b /\
      (Nat.divide a b \/ Nat.divide b a).
Proof.
  intros n A elements_bound elements_NoDup elements_size.
(*@c.step@[[2]][[Top-level CIC endpoint. We restate the final divisibility theorem at the package boundary by combining the abstract pigeonhole route with the odd-part arithmetic route.]]@*)
(*@template.qedinfo@*)
(*@box.section@[[PROPOSITIO]]@*)
(*@box.subsection@[[Second Layer]]@*)
(*@box.astrx.just@[[There is no finitely supported row `u` whose one-step Rule 30 image is exactly the centered seed row. A single seeded defect cannot be created in one forward step by a finitely supported predecessor.]]@*)
(*@box.astrx.cent@[[There is no finitely supported row `u` whose one-step Rule 30 image is exactly the centered seed row. A single seeded defect cannot be created in one forward step by a finitely supported predecessor.]]@*)
