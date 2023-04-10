

function t(b,cookie) {
        b = r(cookie, b + "=" + C("ly.com"), ";");
        if (b != "-")
            b = b.substring(b.indexOf(".") + 1);
        return b
    }
function r(b, c, d) {
        if (!b || !c || !d)
            return "-";
        var e, g = "-";
        e = b.indexOf(c);
        c = c.indexOf("=") + 1;
        if (e > -1) {
            d = b.indexOf(d, e);
            if (d < 0)
                d = b.length;
            g = b.substring(e + c, d)
        }
        return g
    }
function C(b) {
        if (!b)
            return 1;
        for (var c = 0, d = 0, e = b.length - 1; e >= 0; e--) {
            d = parseInt(b.charCodeAt(e));
            c = (c << 6 & 268435455) + d + (d << 14);
            if ((d = c & 266338304) != 0)
                c ^= d >> 21
        }
        return c
    }


function get_dctrack(cookie) {
    ca = t("__tctma",cookie);
    cb = t("__tctmb",cookie);
    dctrack = ["1",ca.split(".")[0], ca.split(".")[4], cb.split(".")[3], cb.split(".")[0], "0"].join('ˇ');
    return dctrack
}
var cookie = 'NewProvinceId=6; NCid=91; NewProvinceName=%E5%B9%BF%E4%B8%9C; NCName=%E6%B7%B1%E5%9C%B3; __tctmu=144323752.0.0; longKey=167696968473806; __tctrack=0; Hm_lvt_64941895c0a12a3bdeb5b07863a52466=1676969694,1677573749; H5CookieId=1fca5a4e-75aa-44cd-bf37-3966c655038c; Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677573758; dj-meta=%257B%2522ttf%2522%3A%252211011010110111110001001101111100010110011111000%257C1011011110000001101000%2522%2C%2522tz%2522%3A-480%2C%2522au%2522%3A%252248000_2_1_0_2_explicit_speakers%2522%2C%2522gp%2522%3A%2522Google%2520Inc.%2520(Intel%2520Inc.)%40ANGLE%2520(Intel%2520Inc.%2C%2520Intel(R)%2520Iris(TM)%2520Plus%2520Graphics%2520OpenGL%2520Engine%2C%2520OpenGL%25204.1)%2522%2C%2522cv%2522%3A%25222d58a52d428e99d1e377c9376b06732049d1ef27%2522%2C%2522pls%2522%3A%2522PDF%2520ViewerChrome%2520PDF%2520ViewerChromium%2520PDF%2520ViewerMicrosoft%2520Edge%2520PDF%2520ViewerWebKit%2520builtin%2520PDF%2522%2C%2522hd%2522%3A%2522zh-CN_zh_8%2522%2C%2522sc%2522%3A%2522900_1440_30_2%2522%2C%2522ua%2522%3A%2522Mozilla%2F5.0%2520(Macintosh%3B%2520Intel%2520Mac%2520OS%2520X%252010_15_7)%2520AppleWebKit%2F537.36%2520(KHTML%2C%2520like%2520Gecko)%2520Chrome%2F110.0.0.0%2520Safari%2F537.36%2522%2C%2522ft%2522%3A%25229ed34b46ca3c1706db122622a6685455e3f082e7%2522%2C%2522lg%2522%3A%25224a95d43fd6e3dc68abc0444e278484fc8432c22c%2522%257D; _ga=GA1.2.605122596.1677573761; __tctmz=144323752.1677652965859.3.2.utmccn=(referral)|utmcsr=google.com|utmcct=|utmcmd=referral; udc_feedback=%7B%22url%22%3A%20%22https%3A%2F%2Fgny.ly.com%2F%22%2C%22platform%22%3A%20%22PC%22%2C%22channel%22%3A%20%22%E5%9B%BD%E5%86%85%E6%B8%B8%22%2C%22page%22%3A%20%22%E5%9B%BD%E5%86%85%E8%AF%A6%E6%83%85%E9%A1%B5%22%7D; pt__search_from=channel=scenery&page=scenery-index; wwwscenery=e63385c94ba81a32d30bcedf71ec319f; pagestate=1; Hm_lpvt_64941895c0a12a3bdeb5b07863a52466=1677657686; __tctma=144323752.167696968473806.1676969684373.1677652965859.1677657690291.4; indexTopSearchHistory=%5B%22%E5%9B%9B%E5%B7%9D%22%2C%22%E5%8E%A6%E9%97%A8%22%5D; 17uCNRefId=RefId=14211829&SEFrom=so&SEKeyWords=; TicketSEInfo=RefId=14211829&SEFrom=so&SEKeyWords=; CNSEInfo=RefId=14211829&tcbdkeyid=&SEFrom=so&SEKeyWords=&RefUrl=https%3A%2F%2Fso.ly.com%2F; qdid=28045|1|14211829|40699c,35294|1|14211860|be6ca5,28045|1|14211829|40699c; Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677657751; __tctmc=144323752.100710275; __tctmd=144323752.205791637; __tctmb=144323752.1876228845978307.1677657835208.1677657835208.1; __tccgd=144323752.0'

console.log(get_dctrack(cookie));