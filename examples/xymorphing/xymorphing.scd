l = Liveness();

for (0, 1, {
    |index| l.addControl(\SimpleKnob, index, { arg addr, value; value.postln; })
});
