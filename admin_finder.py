import requests
import threading
import queue
import colorama
from colorama import Fore, Style
import sys

colorama.init(autoreset=True)

# Load the full admin path list
admin_paths = [
         "/acceso.asp", "/acceso.php", "/access/", "/access.php", "/account/", "/account.asp",
    "/account.html", "/account.php", "/acct_login/", "/_adm_/", "/_adm/", "/adm/", "/adm2/",
    "/adm/admloginuser.asp", "/adm/admloginuser.php", "/adm.asp", "/adm_auth.asp", "/adm_auth.php",
    "/adm.html", "/_admin_/", "/_admin/", "/admin/", "/Admin/", "/ADMIN/", "/admin1/", "/admin1.asp",
    "/admin1.html", "/admin1.php", "/admin2/", "/admin2.asp", "/admin2.html", "/admin2/index/",
    "/admin2/index.asp", "/admin2/index.php", "/admin2/login.asp", "/admin2/login.php", "/admin2.php",
    "/admin3/", "/admin4/", "/admin4_account/", "/admin4_colon/", "/admin5/", "/admin/account.asp",
    "/admin/account.html", "/admin/account.php", "/admin/add_banner.php/", "/admin/addblog.php",
    "/admin/add_gallery_image.php", "/admin/add.php", "/admin/add-room.php", "/admin/add-slider.php",
    "/admin/add_testimonials.php", "/admin/admin/", "/admin/adminarea.php", "/admin/admin.asp",
    "/admin/AdminDashboard.php", "/admin/admin-home.php", "/admin/AdminHome.php", "/admin/admin.html",
    "/admin/admin_index.php", "/admin/admin_login.asp", "/admin/admin-login.asp", "/admin/adminLogin.asp",
    "/admin/admin_login.html", "/admin/admin-login.html", "/admin/adminLogin.html", "/admin/admin_login.php",
    "/admin/admin-login.php", "/admin/adminLogin.php", "/admin/admin_management.php", "/admin/admin.php",
    "/admin/admin_users.php", "/admin/adminview.php", "/admin/adm.php", "/admin_area/", "/adminarea/",
    "/admin_area/admin.asp", "/adminarea/admin.asp", "/admin_area/admin.html", "/adminarea/admin.html",
    "/admin_area/admin.php", "/adminarea/admin.php", "/admin_area/index.asp", "/adminarea/index.asp",
    "/admin_area/index.html", "/adminarea/index.html", "/admin_area/index.php", "/adminarea/index.php",
    "/admin_area/login.asp", "/adminarea/login.asp", "/admin_area/login.html", "/adminarea/login.html",
    "/admin_area/login.php", "/adminarea/login.php", "/admin.asp", "/admin/banner.php", "/admin/banners_report.php",
    "/admin/category.php", "/admin/change_gallery.php", "/admin/checklogin.php", "/admin/configration.php",
    "/admincontrol.asp", "/admincontrol.html", "/admincontrol/login.asp", "/admincontrol/login.html",
    "/admincontrol/login.php", "/admin/control_pages/admin_home.php", "/admin/controlpanel.asp",
    "/admin/controlpanel.html", "/admin/controlpanel.php", "/admincontrol.php", "/admincontrol.php/",
    "/admin/cpanel.php", "/admin/cp.asp", "/admin/CPhome.php", "/admin/cp.html", "/admincp/index.asp",
    "/admincp/index.html", "/admincp/login.asp", "/admin/cp.php", "/admin/dashboard/index.php",
    "/admin/dashboard.php", "/admin/dashbord.php", "/admin/dash.php", "/admin/default.php", "/adm/index.asp",
    "/adm/index.html", "/adm/index.php", "/admin/enter.php", "/admin/event.php", "/admin/form.php",
    "/admin/gallery.php", "/admin/headline.php", "/admin/home.asp", "/admin/home.html", "/admin_home.php",
    "/admin/home.php", "/admin.html", "/admin/index.asp", "/admin/index-digital.php", "/admin/index.html",
    "/admin/index.php", "/admin/index_ref.php", "/admin/initialadmin.php", "/administer/", "/administr8/",
    "/administr8.asp", "/administr8.html", "/administr8.php", "/administracion.php", "/administrador/",
    "/administratie/", "/administration/", "/administration.html", "/administration.php", "/administrator",
    "/_administrator_/", "/_administrator/", "/administrator/", "/administrator/account.asp",
    "/administrator/account.html", "/administrator/account.php", "/administratoraccounts/", "/administrator.asp",
    "/administrator.html", "/administrator/index.asp", "/administrator/index.html", "/administrator/index.php",
    "/administratorlogin/", "/administrator/login.asp", "/administratorlogin.asp", "/administrator/login.html",
    "/administrator/login.php", "/administratorlogin.php", "/administratorlogin.php", "/administrator.php",
    "/administrators/", "/administrivia/", "/admin/leads.php", "/admin/list_gallery.php", "/admin/login",
    "/adminLogin/", "/admin_login.asp", "/admin-login.asp", "/admin/login.asp", "/adminLogin.asp",
    "/admin/login-home.php", "/admin_login.html", "/admin-login.html", "/admin/login.html", "/adminLogin.html",
    "/ADMIN/login.html", "/admin_login.php", "/admin-login.php", "/admin-login.php/", "/admin/login.php",
    "/adminLogin.php", "/ADMIN/login.php", "/admin/login_success.php", "/admin/loginsuccess.php", "/admin/log.php",
    "/admin_main.html", "/admin/main_page.php", "/admin/main.php/", "/admin/ManageAdmin.php",
    "/admin/manageImages.php", "/admin/manage_team.php", "/admin/member_home.php", "/admin/moderator.php",
    "/admin/my_account.php", "/admin/myaccount.php", "/admin/overview.php", "/admin/page_management.php",
    "/admin/pages/home_admin.php", "/adminpanel/", "/adminpanel.asp", "/adminpanel.html", "/adminpanel.php",
    "/admin.php", "/Admin/private/", "/adminpro/", "/admin/product.php", "/admin/products.php", "/admins/",
    "/admins.asp", "/admin/save.php", "/admins.html", "/admin/slider.php", "/admin/specializations.php",
    "/admins.php", "/admin_tool/", "/AdminTools/", "/admin/uhome.html", "/admin/upload.php",
    "/admin/userpage.php", "/admin/viewblog.php", "/admin/viewmembers.php", "/admin/voucher.php",
    "/AdminWeb/", "/admin/welcomepage.php", "/admin/welcome.php", "/admloginuser.asp", "/admloginuser.php",
    "/admon/", "/ADMON/", "/adm.php", "/affiliate.asp", "/affiliate.php", "/auth/", "/auth/login/",
    "/authorize.php", "/autologin/", "/banneradmin/", "/base/admin/", "/bb-admin/", "/bbadmin/",
    "/bb-admin/admin.asp", "/bb-admin/admin.html", "/bb-admin/admin.php", "/bb-admin/index.asp",
    "/bb-admin/index.html", "/bb-admin/index.php", "/bb-admin/login.asp", "/bb-admin/login.html",
    "/bb-admin/login.php", "/bigadmin/", "/blogindex/", "/cadmins/", "/ccms/", "/ccms/index.php",
    "/ccms/login.php", "/ccp14admin/", "/cms/", "/cms/admin/", "/cmsadmin/", "/cms/_admin/logon.php",
    "/cms/login/", "/configuration/", "/configure/", "/controlpanel/", "/controlpanel.asp",
    "/controlpanel.html", "/controlpanel.php", "/cpanel/", "/cPanel/", "/cpanel_file/", "/cp.asp", "/cp.html",
    "/cp.php", "/customer_login/", "/database_administration/", "/Database_Administration/", "/db/admin.php",
    "/directadmin/", "/dir-login/", "/editor/", "/edit.php", "/evmsadmin/", "/ezsqliteadmin/", "/fileadmin/",
    "/fileadmin.asp", "/fileadmin.html", "/fileadmin.php", "/formslogin/", "/forum/admin", "/globes_admin/",
    "/home.asp", "/home.html", "/home.php", "/hpwebjetadmin/", "/include/admin.php", "/includes/login.php",
    "/Indy_admin/", "/instadmin/", "/interactive/admin.php", "/irc-macadmin/", "/links/login.php",
    "/LiveUser_Admin/", "/login/", "/login1/", "/login.asp", "/login_db/", "/loginflat/", "/login.html",
    "/login/login.php", "/login.php", "/login-redirect/", "/logins/", "/login-us/", "/logon/", "/logo_sysadmin/",
    "/Lotus_Domino_Admin/", "/macadmin/", "/mag/admin/", "/maintenance/", "/manage_admin.php", "/manager/",
    "/manager/ispmgr/", "/manuallogin/", "/memberadmin/", "/memberadmin.asp", "/memberadmin.php", "/members/",
    "/memlogin/", "/meta_login/", "/modelsearch/admin.asp", "/modelsearch/admin.html", "/modelsearch/admin.php",
    "/modelsearch/index.asp", "/modelsearch/index.html", "/modelsearch/index.php", "/modelsearch/login.asp",
    "/modelsearch/login.html", "/modelsearch/login.php", "/moderator/", "/moderator/admin.asp",
    "/moderator/admin.html", "/moderator/admin.php", "/moderator.asp", "/moderator.html",
    "/moderator/login.asp", "/moderator/login.html", "/moderator/login.php", "/moderator.php", "/moderator.php/",
    "/myadmin/", "/navSiteAdmin/", "/newsadmin/", "/nsw/admin/login.php", "/openvpnadmin/",
    "/pages/admin/admin-login.asp", "/pages/admin/admin-login.html", "/pages/admin/admin-login.php",
    "/panel/", "/panel-administracion/", "/panel-administracion/admin.asp", "/panel-administracion/admin.html",
    "/panel-administracion/admin.php", "/panel-administracion/index.asp", "/panel-administracion/index.html",
    "/panel-administracion/index.php", "/panel-administracion/login.asp", "/panel-administracion/login.html",
    "/panel-administracion/login.php", "/panelc/", "/paneldecontrol/", "/panel.php", "/pgadmin/",
    "/phpldapadmin/", "/phpmyadmin/", "/phppgadmin/", "/phpSQLiteAdmin/", "/platz_login/", "/pma/",
    "/power_user/", "/project-admins/", "/pureadmin/", "/radmind/", "/radmind-1/", "/rcjakar/admin/login.php",
    "/rcLogin/", "/server/", "/Server/", "/ServerAdministrator/", "/server_admin_small/", "/Server.asp",
    "/Server.html", "/Server.php", "/showlogin/", "/simpleLogin/", "/site/admin/", "/siteadmin/",
    "/siteadmin/index.asp", "/siteadmin/index.php", "/siteadmin/login.asp", "/siteadmin/login.html",
    "/site_admin/login.php", "/siteadmin/login.php", "/smblogin/", "/sql-admin/", "/sshadmin/",
    "/ss_vms_admin_sm/", "/staradmin/", "/sub-login/", "/Super-Admin/", "/support_login/", "/sys-admin/",
    "/sysadmin/", "/SysAdmin/", "/SysAdmin2/", "/sysadmin.asp", "/sysadmin.html", "/sysadmin.php",
    "/sysadmins/", "/system_administration/", "/system-administration/", "/typo3/", "/ur-admin/",
    "/ur-admin.asp", "/ur-admin.html", "/ur-admin.php", "/useradmin/", "/user.asp", "/user.html",
    "/UserLogin/", "/user.php", "/usuario/", "/usuarios/", "/usuarios//", "/usuarios/login.php",
    "/utility_login/", "/vadmind/", "/vmailadmin/", "/webadmin/", "/WebAdmin/", "/webadmin/admin.asp",
    "/webadmin/admin.html", "/webadmin/admin.php", "/webadmin.asp", "/webadmin.html", "/webadmin/index.asp",
    "/webadmin/index.html", "/webadmin/index.php", "/webadmin/login.asp", "/webadmin/login.html",
    "/webadmin/login.php", "/webadmin.php", "/webmaster/", "/websvn/", "/wizmysqladmin/", "/wp-admin/",
    "/wp-login/", "/wplogin/", "/wp-login.php", "/xlogin/", "/yonetici.asp", "/yonetici.html", "/yonetici.php",
    "/yonetim.asp", "/yonetim.html", "/yonetim.php""/admin/", "/administrator/", "/admin1/", "/admin2/", "/admin3/", "/admin4/", "/admin5/",
    "/usuarios/", "/usuario/", "/moderator/", "/webadmin/", "/adminarea/", "/bb-admin/",
    "/adminLogin/", "/admin_area/", "/panel-administracion/", "/instadmin/", "/memberadmin/",
    "/administratorlogin/", "/adm/", "/admin/account.php", "/admin/index.php", "/admin/login.php",
    "/admin/admin.php", "/admin_area/admin.php", "/admin_area/login.php", "/siteadmin/login.php",
    "/siteadmin/index.php", "/siteadmin/login.html", "/admin/account.html", "/admin/index.html",
    "/admin/login.html", "/admin/admin.html", "/admin_area/index.php", "/bb-admin/index.php",
    "/bb-admin/login.php", "/bb-admin/admin.php", "/admin/home.php", "/admin_area/login.html",
    "/admin_area/index.html", "/admin/controlpanel.php", "/admin.php", "/admincp/index.asp",
    "/admincp/login.asp", "/admincp/index.html", "/adminpanel.html", "/webadmin.html",
    "/webadmin/index.html", "/webadmin/admin.html", "/webadmin/login.html", "/admin/admin_login.html",
    "/admin_login.html", "/panel-administracion/login.html", "/admin/cp.php", "/cp.php",
    "/administrator/index.php", "/administrator/login.php", "/nsw/admin/login.php",
    "/webadmin/login.php", "/admin/admin_login.php", "/admin_login.php", "/administrator/account.php",
    "/administrator.php", "/admin_area/admin.html", "/pages/admin/admin-login.php",
    "/admin/admin-login.php", "/admin-login.php", "/bb-admin/index.html", "/bb-admin/login.html",
    "/acceso.php", "/bb-admin/admin.html", "/admin/home.html", "/login.php",
    "/modelsearch/login.php", "/moderator.php", "/moderator/login.php", "/moderator/admin.php",
    "/account.php", "/pages/admin/admin-login.html", "/admin/admin-login.html", "/admin-login.html",
    "/controlpanel.php", "/admincontrol.php", "/adminLogin.html", "/home.html",
    "/rcjakar/admin/login.php", "/adminarea/index.html", "/adminarea/admin.html", "/webadmin.php",
    "/webadmin/index.php", "/webadmin/admin.php", "/admin/controlpanel.html", "/admin.html",
    "/admin/cp.html", "/cp.html", "/adminpanel.php", "/moderator.html", "/administrator/index.html",
    "/administrator/login.html", "/user.html", "/administrator/account.html", "/administrator.html",
    "/login.html", "/modelsearch/login.html", "/moderator/login.html", "/adminarea/login.html",
    "/panel-administracion/index.html", "/panel-administracion/admin.html", "/modelsearch/index.html",
    "/modelsearch/admin.html", "/admincontrol/login.html", "/adm/index.html", "/adm.html",
    "/moderator/admin.html", "/user.php", "/account.html", "/controlpanel.html", "/admincontrol.html",
    "/panel-administracion/login.php", "/wp-login.php", "/adminLogin.php", "/home.php",
    "/adminarea/index.php", "/adminarea/admin.php", "/adminarea/login.php",
    "/panel-administracion/index.php", "/panel-administracion/admin.php", "/modelsearch/index.php",
    "/modelsearch/admin.php", "/admincontrol/login.php", "/adm/admloginuser.php",
    "/admloginuser.php", "/admin2.php", "/admin2/login.php", "/admin2/index.php",
    "/usuarios/login.php", "/adm/index.php", "/adm.php", "/affiliate.php", "/adm_auth.php",
    "/memberadmin.php", "/administratorlogin.php",
    # ASP
    "/account.asp", "/admin/account.asp", "/admin/index.asp", "/admin/login.asp", "/admin/admin.asp",
    "/admin_area/admin.asp", "/admin_area/login.asp", "/admin_area/index.asp", "/bb-admin/index.asp",
    "/bb-admin/login.asp", "/bb-admin/admin.asp", "/admin/home.asp", "/admin/controlpanel.asp",
    "/admin.asp", "/pages/admin/admin-login.asp", "/admin-login.asp", "/admin/cp.asp", "/cp.asp",
    "/administrator/account.asp", "/administrator.asp", "/acceso.asp", "/login.asp",
    "/modelsearch/login.asp", "/moderator.asp", "/moderator/login.asp", "/administrator/login.asp",
    "/moderator/admin.asp", "/controlpanel.asp", "/adminpanel.asp", "/webadmin.asp",
    "/webadmin/index.asp", "/webadmin/admin.asp", "/webadmin/login.asp", "/admin/admin_login.asp",
    "/admin_login.asp", "/panel-administracion/login.asp", "/adminLogin.asp", "/home.asp",
    "/adminarea/index.asp", "/adminarea/admin.asp", "/adminarea/login.asp",
    "/panel-administracion/index.asp", "/panel-administracion/admin.asp", "/modelsearch/index.asp",
    "/modelsearch/admin.asp", "/administrator/index.asp", "/admincontrol/login.asp",
    "/adm/admloginuser.asp", "/admloginuser.asp", "/admin2.asp", "/admin2/login.asp",
    "/admin2/index.asp", "/adm/index.asp", "/adm.asp", "/affiliate.asp", "/adm_auth.asp",
    "/memberadmin.asp", "/administratorlogin.asp", "/siteadmin/login.asp", "/siteadmin/index.asp",
    # CFM
    "/admin/account.cfm", "/admin/index.cfm", "/admin/login.cfm", "/admin/admin.cfm",
    "/admin_area/admin.cfm", "/admin_area/login.cfm", "/siteadmin/login.cfm", "/siteadmin/index.cfm",
    "/admin_area/index.cfm", "/bb-admin/index.cfm", "/bb-admin/login.cfm", "/bb-admin/admin.cfm",
    "/admin/home.cfm", "/admin/controlpanel.cfm", "/admin.cfm", "/admin/cp.cfm", "/cp.cfm",
    "/administrator/index.cfm", "/administrator/login.cfm", "/nsw/admin/login.cfm",
    "/webadmin/login.cfm", "/admin/admin_login.cfm", "/admin_login.cfm", "/administrator/account.cfm",
    "/administrator.cfm", "/pages/admin/admin-login.cfm", "/admin/admin-login.cfm", "/admin-login.cfm",
    "/login.cfm", "/modelsearch/login.cfm", "/moderator.cfm", "/moderator/login.cfm",
    "/moderator/admin.cfm", "/account.cfm", "/controlpanel.cfm", "/admincontrol.cfm",
    "/rcjakar/admin/login.cfm", "/webadmin.cfm", "/webadmin/index.cfm", "/webadmin/admin.cfm",
    "/adminpanel.cfm", "/panel-administracion/login.cfm", "/wp-login.cfm", "/adminLogin.cfm",
    "/home.cfm", "/adminarea/index.cfm", "/adminarea/admin.cfm", "/adminarea/login.cfm",
    "/panel-administracion/index.cfm", "/panel-administracion/admin.cfm", "/modelsearch/index.cfm",
    "/modelsearch/admin.cfm", "/admincontrol/login.cfm", "/adm/admloginuser.cfm",
    "/admloginuser.cfm", "/admin2.cfm", "/admin2/login.cfm", "/admin2/index.cfm",
    "/usuarios/login.cfm", "/adm/index.cfm", "/adm.cfm", "/affiliate.cfm", "/adm_auth.cfm",
    "/memberadmin.cfm", "/administratorlogin.cfm",
    # JS
    "/admin/account.js", "/admin/index.js", "/admin/login.js", "/admin/admin.js",
    "/admin_area/admin.js", "/admin_area/login.js", "/siteadmin/login.js", "/siteadmin/index.js",
    "/admin_area/index.js", "/bb-admin/index.js", "/bb-admin/login.js", "/bb-admin/admin.js",
    "/admin/home.js", "/admin/controlpanel.js", "/admin.js", "/admin/cp.js", "/cp.js",
    "/administrator/index.js", "/administrator/login.js", "/nsw/admin/login.js",
    "/webadmin/login.js", "/admin/admin_login.js", "/admin_login.js", "/administrator/account.js",
    "/administrator.js", "/pages/admin/admin-login.js", "/admin/admin-login.js", "/admin-login.js",
    "/login.js", "/modelsearch/login.js", "/moderator.js", "/moderator/login.js",
    "/moderator/admin.js", "/account.js", "/controlpanel.js", "/admincontrol.js",
    "/rcjakar/admin/login.js", "/webadmin.js", "/webadmin/index.js", "/webadmin/admin.js",
    "/adminpanel.js", "/panel-administracion/login.js", "/wp-login.js", "/adminLogin.js",
    "/home.js", "/adminarea/index.js", "/adminarea/admin.js", "/adminarea/login.js",
    "/panel-administracion/index.js", "/panel-administracion/admin.js", "/modelsearch/index.js",
    "/modelsearch/admin.js", "/admincontrol/login.js", "/adm/admloginuser.js", "/admloginuser.js",
    "/admin2.js", "/admin2/login.js", "/admin2/index.js", "/usuarios/login.js", "/adm/index.js",
    "/adm.js", "/affiliate.js", "/adm_auth.js", "/memberadmin.js", "/administratorlogin.js",
    # CGI
    "/admin/account.cgi", "/admin/index.cgi", "/admin/login.cgi", "/admin/admin.cgi",
    "/admin_area/admin.cgi", "/admin_area/login.cgi", "/siteadmin/login.cgi", "/siteadmin/index.cgi",
    "/admin_area/index.cgi", "/bb-admin/index.cgi", "/bb-admin/login.cgi", "/bb-admin/admin.cgi",
    "/admin/home.cgi", "/admin/controlpanel.cgi", "/admin.cgi", "/admin/cp.cgi", "/cp.cgi",
    "/administrator/index.cgi", "/administrator/login.cgi", "/nsw/admin/login.cgi",
    "/webadmin/login.cgi", "/admin/admin_login.cgi", "/admin_login.cgi", "/administrator/account.cgi",
    "/administrator.cgi", "/pages/admin/admin-login.cgi", "/admin/admin-login.cgi", "/admin-login.cgi",
    "/login.cgi", "/modelsearch/login.cgi", "/moderator.cgi", "/moderator/login.cgi",
    "/moderator/admin.cgi", "/account.cgi", "/controlpanel.cgi", "/admincontrol.cgi",
    "/rcjakar/admin/login.cgi", "/webadmin.cgi", "/webadmin/index.cgi", "/webadmin/admin.cgi",
    "/adminpanel.cgi", "/panel-administracion/login.cgi", "/wp-login.cgi", "/adminLogin.cgi",
    "/home.cgi", "/adminarea/index.cgi", "/adminarea/admin.cgi", "/adminarea/login.cgi",
    "/panel-administracion/index.cgi", "/panel-administracion/admin.cgi", "/modelsearch/index.cgi",
    "/modelsearch/admin.cgi", "/admincontrol/login.cgi", "/adm/admloginuser.cgi", "/admloginuser.cgi",
    "/admin2.cgi", "/admin2/login.cgi", "/admin2/index.cgi", "/usuarios/login.cgi", "/adm/index.cgi",
    "/adm.cgi", "/affiliate.cgi", "/adm_auth.cgi", "/memberadmin.cgi", "/administratorlogin.cgi"
]

# Define settings
NUM_THREADS = 10
timeout = 3

def scan_url(base_url, path, verbose):
    url = base_url + path
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(Fore.GREEN + "[+] Found: " + url)
        else:
            if verbose:
                print(Fore.RED + f"[-] Not Found ({response.status_code}): {url}")
    except requests.RequestException:
        if verbose:
            print(Fore.RED + "[-] Connection Error: " + url)

def worker(q, base_url, verbose):
    while not q.empty():
        path = q.get()
        scan_url(base_url, path, verbose)
        q.task_done()

def main():
    print(Style.BRIGHT + Fore.CYAN + "🔥 Admin Panel Finder - Turbo Scan Edition 🔥")
    
    target = input(Fore.YELLOW + "[*] Enter target URL (e.g., https://example.com): ").strip()
    if not target.startswith("http"):
        print(Fore.RED + "[!] Please include http:// or https:// in the URL.")
        sys.exit(1)

    verbose_input = input(Fore.YELLOW + "[*] Enable verbose mode? (y/n): ").lower().strip()
    verbose = verbose_input == 'y'

    q = queue.Queue()
    for path in admin_paths:
        q.put(path)

    print(Fore.BLUE + f"[*] Starting scan on {target} with {NUM_THREADS} threads...")

    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(q, target, verbose))
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    print(Style.BRIGHT + Fore.GREEN + "[✓] Scan completed.")

if __name__ == "__main__":
    main()
