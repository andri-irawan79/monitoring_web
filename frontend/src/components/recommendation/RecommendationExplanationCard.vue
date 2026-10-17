<script setup>
import BaseCard from "../ui/BaseCard.vue";

defineProps({

    fuzzy:{
        type:Object,
        default:()=>({})
    },

    rule:{
        type:Object,
        default:()=>({})
    },

    recommendation:{
        type:Object,
        default:()=>({})
    },

    defuzzification:{
        type:Object,
        default:()=>({})
    }

});

const dominantCategory = (obj) => {

    if (!obj){

        return{

            label:"-",
            value:"-"

        };

    }

    let max = -1;
    let label = "-";

    Object.entries(obj).forEach(([k,v])=>{

        if(v > max){

            max = v;
            label = k;

        }

    });

    return{

        label,

        value:Number(max).toFixed(3)

    };

};

</script>

<template>

<BaseCard>

<h2 class="text-2xl font-bold mb-6">

💡 Penjelasan Sistem

</h2>

<div class="space-y-5">

<div>

<h3 class="font-semibold text-green-700">

Hasil Fuzzifikasi

</h3>

<ul class="mt-3 space-y-2 list-disc ml-6">

<li>

Nitrogen berada pada kategori

<b>

{{ dominantCategory(fuzzy.N).label }}

</b>

dengan derajat keanggotaan

<b>

{{ dominantCategory(fuzzy.N).value }}

</b>

</li>

<li>

Fosfor berada pada kategori

<b>

{{ dominantCategory(fuzzy.P).label }}

</b>

dengan derajat keanggotaan

<b>

{{ dominantCategory(fuzzy.P).value }}

</b>

</li>

<li>

Kalium berada pada kategori

<b>

{{ dominantCategory(fuzzy.K).label }}

</b>

dengan derajat keanggotaan

<b>

{{ dominantCategory(fuzzy.K).value }}

</b>

</li>

<li>

pH berada pada kategori

<b>

{{ dominantCategory(fuzzy.PH).label }}

</b>

dengan derajat keanggotaan

<b>

{{ dominantCategory(fuzzy.PH).value }}

</b>

</li>

</ul>

</div>

<hr>

<div>

<h3 class="font-semibold text-green-700">

Rule Dominan

</h3>

<p class="mt-2">

Rule

<b>

R{{ rule.rule_id }}

</b>

memiliki nilai α terbesar yaitu

<b>

{{ rule.alpha }}

</b>

sehingga dipilih sebagai rule dominan.

</p>

</div>

<hr>

<div>

<h3 class="font-semibold text-green-700">

Defuzzifikasi

</h3>

<p class="mt-2">

Nilai akhir diperoleh menggunakan metode Tsukamoto:

</p>

<p class="font-bold mt-3">

Σ(α × z) / Σα

</p>

<p>

=

{{ defuzzification.alpha_z }}

/

{{ defuzzification.alpha }}

</p>

<p class="mt-2">

=

<b>

{{ defuzzification.hasil }}

kg/pohon

</b>

</p>

</div>

<hr>

<div
class="bg-green-50 border border-green-200 rounded-xl p-5">

<h3 class="font-semibold text-green-700">

Kesimpulan

</h3>

<p class="mt-3">

Berdasarkan hasil fuzzifikasi,
evaluasi rule,
dan proses defuzzifikasi,
sistem merekomendasikan penggunaan

<b>

{{ recommendation.jenis_pupuk }}

</b>

dengan dosis

<b>

{{ recommendation.dosis }}

kg/pohon

</b>

karena kondisi nutrisi tanaman paling sesuai dengan rule dominan yang aktif.

</p>

</div>

</div>

</BaseCard>

</template>
