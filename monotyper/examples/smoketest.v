(*@file@*)

(*@section@[[SPARSE SYNTAX]]@*)

(*@inline@[[Small directives keep the annotated Rocq source close to the proof while Monotyper takes care of the presentation.]]@*)

From Stdlib Require Import Arith.

(*@unicode@[[ Minimal input; regular output. ]]@*)

(*@unicodemath@[[∀ n ∈ ℕ, n + 0 = n]][[∀ n ∈ ℕ, 0 + n = n]]@*)

Theorem add_zero_right :
  forall n : nat,
    n + 0 = n.
Proof.
  (*@inline@[[The standard library already provides the right-neutrality law.]]@*)
  intro n.
  apply Nat.add_0_r.
Qed.
