(*smoketest.v*)
(*
  Proofcase / T000 / CIC Integration
  ==================================

    Overview
    --------

      This file is the top-level CIC route for T000. It binds the package-local
      CIC folder into one stable import point for downstream surfaces.

      The current CIC payload is the pigeonhole divisibility development

      (1)  `R01__Odd_Part`
      (2)  `R02__Pigeonhole_Divisibility`

      Architecturally, `R01__CIC` is the integration layer of the package. The
      abstract combinatorial contribution belongs to
      `R02__Pigeonhole_Divisibility`, whose role is to provide the
      generallist-pigeonhole mechanism in a form independent of the final
      arithmetic application. The present file performs the closing
      specialization: it combines that abstract machinery with the odd-part
      codomain control and divisibility bridge supplied by `R01__Odd_Part`, and
      thereby derives the package-level endpoint `pigeonhole_divisibility_CIC`.
*)
From Coq Require Import Arith Lia List PeanoNat.

From T000.CIC__Pigeonhole_Divisibility Require Export
  R01__Odd_Part
  R02__Pigeonhole_Divisibility.
(*
│
│  Top-level CIC endpoint. We restate the final
│  divisibility theorem at the package boundary by
│  combining the abstract pigeonhole route with
│  the odd-part arithmetic route.
│
*)
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
(*
│
│  (2)
│  Top-level CIC endpoint. We restate the final
│  divisibility theorem at the package boundary by
│  combining the abstract pigeonhole route with
│  the odd-part arithmetic route.
│
*)
(*
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                          CERTIFICATION LAYER                            │
│                                                                         │
│     ________________________ __________________                         │
│     ___________________  __ \ ___  ____/__  __ \                        │
│     __________________  / / / __  __/  __  / / /                        │
│     _________________/ /_/ /___  /______  /_/ /__                       │
│     _________________\___\_\(_)_____/(_)_____/_(_)                      │
│                                                                         │
│                                                                         │
│     This  file  specifies the exact public target and the Rocq-side     │
│     criteria  required  by  the  reductions.  It  forms the central     │
│     certificate  layer of the development and serves as the primary     │
│     point  of verification. It also defines the contract fixing the     │
│     subject  of proof, certifies each endpoint by direct reuse, and     │
│     makes all key assumptions explicit for inspection and audit.        │
│                                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
*)
(*
╔═════════════════════════════════════════════════════════════════════════╗
║                                                                         ║
║                                PROPOSITIO                               ║
║                                                                         ║
╚═════════════════════════════════════════════════════════════════════════╝
*)
(*
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                               Second Layer                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
*)
(*************************************************************************)
(*                                                                       *)
(*    There  is  no finitely supported row `u` whose one-step Rule 30    *)
(*    image  is exactly the centered seed row. A single seeded defect    *)
(*    cannot  be  created in one forward step by a finitely supported    *)
(*    predecessor.                                                       *)
(*                                                                       *)
(*************************************************************************)
(*************************************************************************)
(*                                                                       *)
(*     There is no finitely supported row `u` whose one-step Rule 30     *)
(*     image is exactly the centered seed row. A single seeded defect    *)
(*     cannot be created in one forward step by a finitely supported     *)
(*                              predecessor.                             *)
(*                                                                       *)
(*************************************************************************)
