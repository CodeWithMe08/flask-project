

/*animations and transitions*/
gsap.registerPlugin(ScrollTrigger);
var tl = gsap.timeline();

tl.from('.content', {
    y: '-30%',
    opacity: 0,
    duration: 2,
    ease: Power4.easeOut
})
tl.from('.stagger1', {
    opacity: 0,
    y: -50,
    stagger: .3,
    ease: Power4.easeOut,
    duration: 2
}, "-=1.5")
tl.from('.hero-design', {
    opacity: 0, y: 50, ease: Power4.easeOut, duration: 1
}, "-=2")

gsap.from(".square-anim", {
    stagger: .2,
    scale: 0.1,
    duration: 1,
    ease: Back.easeOut.config(1.7)
})

gsap.from(".transition2", {
    scrollTrigger: {
        trigger: '.transition2',
        start: "top bottom"
    },
    y: 50,
    opacity: 0,
    duration: 1.2,
    stagger: .3
})

gsap.from(".transition3", {
    scrollTrigger: {
        trigger: ".transition3",
        start: "top bottom"
    },
    y: 50,
    opacity: 0,
    duration: 1.2,
    stagger: .3
})
gsap.from(".transition4", {
    scrollTrigger: {
        trigger: ".transition4",
        start: "top center"
    },
    y: 50,
    opacity: 0,
    duration: 1.2,
    stagger: .5
})
gsap.from(".transition5", {
    scrollTrigger: {
        trigger: ".transition5",
        start: "bottom center"
    },
    y: 50,
    opacity: 0,
    duration: 1.2,
    stagger: .6
});


    /*admin panel*/
document.getElementById('admin08').addEventListener("click", function() {
    document.querySelector('.bg-modals').style.display = "flex";
    });
        
document.querySelector('.closes').addEventListener("click", function() {
    document.querySelector('.bg-modals').style.display = "none";
    });
