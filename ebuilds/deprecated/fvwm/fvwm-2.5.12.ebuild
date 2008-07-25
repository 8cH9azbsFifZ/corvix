#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="fvwm"
HOMEPAGE="http://www.fvwm.org"
SRC_URI="ftp://ftp.fvwm.org/pub/$ENAME/version-2/$ENAME-$EVERS.tar.bz2"

DEPEND="aterm gmrun trayer habak conky gsetroot vim-vimoutliner rxvt-unicode rxvt xterm unclutter ipython picasa thunar k3b pidgin kphone"
SDEPEND="fvwm"

LICENSE="abc"

PREFIX=/tmp

src_unpack() {
}

src_configure() {
   #epatch ../fvwm-translucency.diff 
   #rr autoconf
   #rr aclocal
   #rr automake
   #econfigure --disable-bidi
}

src_compile() {
   #emake -j 4
}

src_install() {
#   einstall
}  

post_inst() {
   elog "Installing Theme..."
}

epatch_fvwm-translucency.diff() {
# original: 
# This is a shell archive (produced by GNU sharutils 4.6.3).
# To extract the files from this archive, save it to some FILE, remove
# everything before the `#!/bin/sh' line above, then type `sh FILE'.
#
lock_dir=_sh04114
# Made on 2008-05-15 21:46 UTC by <gerolf@x61s>.
# Source directory was `/home/gerolf/src/egatrop/var/lib/egatrop/ebuilds/fvwm'.
#
# Existing files will *not* be overwritten, unless `-c' is specified.
#
# This shar contains:
# length mode       name
# ------ ---------- ------------------------------------------
#  11434 -rw------- fvwm-translucency.diff
#
MD5SUM=${MD5SUM-md5sum}
f=`${MD5SUM} --version | egrep '^md5sum .*(core|text)utils'`
test -n "${f}" && md5check=true || md5check=false
${md5check} || \
  echo 'Note: not verifying md5sums.  Consider installing GNU coreutils.'
save_IFS="${IFS}"
IFS="${IFS}:"
gettext_dir=FAILED
locale_dir=FAILED
first_param="$1"
for dir in $PATH
do
  if test "$gettext_dir" = FAILED && test -f $dir/gettext \
     && ($dir/gettext --version >/dev/null 2>&1)
  then
    case `$dir/gettext --version 2>&1 | sed 1q` in
      *GNU*) gettext_dir=$dir ;;
    esac
  fi
  if test "$locale_dir" = FAILED && test -f $dir/shar \
     && ($dir/shar --print-text-domain-dir >/dev/null 2>&1)
  then
    locale_dir=`$dir/shar --print-text-domain-dir`
  fi
done
IFS="$save_IFS"
if test "$locale_dir" = FAILED || test "$gettext_dir" = FAILED
then
  echo=echo
else
  TEXTDOMAINDIR=$locale_dir
  export TEXTDOMAINDIR
  TEXTDOMAIN=sharutils
  export TEXTDOMAIN
  echo="$gettext_dir/gettext -s"
fi
if (echo "testing\c"; echo 1,2,3) | grep c >/dev/null
then if (echo -n test; echo 1,2,3) | grep n >/dev/null
     then shar_n= shar_c='
'
     else shar_n=-n shar_c= ; fi
else shar_n= shar_c='\c' ; fi
f=shar-touch.$$
st1=200112312359.59
st2=123123592001.59
st2tr=123123592001.5 # old SysV 14-char limit
st3=1231235901

if touch -am -t ${st1} ${f} >/dev/null 2>&1 && \
   test ! -f ${st1} && test -f ${f}; then
  shar_touch='touch -am -t $1$2$3$4$5$6.$7 "$8"'

elif touch -am ${st2} ${f} >/dev/null 2>&1 && \
   test ! -f ${st2} && test ! -f ${st2tr} && test -f ${f}; then
  shar_touch='touch -am $3$4$5$6$1$2.$7 "$8"'

elif touch -am ${st3} ${f} >/dev/null 2>&1 && \
   test ! -f ${st3} && test -f ${f}; then
  shar_touch='touch -am $3$4$5$6$2 "$8"'

else
  shar_touch=:
  echo
  ${echo} 'WARNING: not restoring timestamps.  Consider getting and'
  ${echo} 'installing GNU `touch'\'', distributed in GNU coreutils...'
  echo
fi
rm -f ${st1} ${st2} ${st2tr} ${st3} ${f}
#
if test ! -d ${lock_dir}
then : ; else ${echo} 'lock directory '${lock_dir}' exists'
  return 1
fi
if mkdir ${lock_dir}
then ${echo} 'x - created lock directory `'${lock_dir}\''.'
else ${echo} 'x - failed to create lock directory `'${lock_dir}\''.'
  return 1
fi
# ============= fvwm-translucency.diff ==============
if test -f 'fvwm-translucency.diff' && test "$first_param" != -c; then
  ${echo} 'x -SKIPPING fvwm-translucency.diff (file already exists)'
else
${echo} 'x - extracting fvwm-translucency.diff (text)'
  sed 's/^X//' << 'SHAR_EOF' > 'fvwm-translucency.diff' &&
diff -ruN fvwm.orig/fvwm/colorset.c fvwm/fvwm/colorset.c
--- fvwm.orig/fvwm/colorset.c	2004-08-25 07:00:34.302483656 +0100
+++ fvwm/fvwm/colorset.c	2004-08-25 07:00:40.501541256 +0100
@@ -159,7 +159,9 @@
X 	"IconTint",
X 	"NoIconTint",
X 	"IconAlpha",
-
+	
+	"Translucent",
+	"NoTranslucent",
X 	NULL
X };
X 
@@ -616,6 +618,7 @@
X 	char *fg_tint = NULL;
X 	char *bg_tint = NULL;
X 	char *icon_tint = NULL;
+	char *translucent_tint = NULL;
X 	Bool have_pixels_changed = False;
X 	Bool has_icon_pixels_changed = False;
X 	Bool has_fg_changed = False;
@@ -628,6 +631,7 @@
X 	Bool has_fg_tint_changed = False;
X 	Bool has_bg_tint_changed = False;
X 	Bool has_icon_tint_changed = False;
+	Bool has_translucent_tint_changed = False;
X 	Bool has_pixmap_changed = False;
X 	Bool has_shape_changed = False;
X 	Bool has_image_alpha_changed = False;
@@ -754,6 +758,10 @@
X 		case 21: /* Plain */
X 			has_pixmap_changed = True;
X 			free_colorset_background(cs, True);
+			cs->is_translucent = False;
+			cs->translucent_tint_percent = 0;
+			cs->color_flags &= ~TRANSLUCENT_TINT_SUPPLIED;
+			has_translucent_tint_changed = True;
X 			break;
X 		case 22: /* NoShape */
X 			has_shape_changed = True;
@@ -920,6 +928,24 @@
X 				cs->icon_alpha_percent = tmp;
X 			}
X 			break;
+		case 42: /* Translucent */
+			cs->is_translucent = True;
+			parse_simple_tint(
+				cs, args, &translucent_tint,
+				TRANSLUCENT_TINT_SUPPLIED,
+				&has_translucent_tint_changed, &percent,
+				"Translucent");
+			if (has_translucent_tint_changed)
+			{
+				cs->translucent_tint_percent = percent;
+			}
+			break;
+		case 43: /* NoTranslucent */
+			cs->is_translucent = False;
+			cs->translucent_tint_percent = 0;
+			cs->color_flags &= ~TRANSLUCENT_TINT_SUPPLIED;
+			has_translucent_tint_changed = True;
+			break;
X 		default:
X 			/* test for ?Gradient */
X 			if (option[0] && StrEquals(&option[1], "Gradient"))
@@ -1604,6 +1630,27 @@
X 		}
X 	}
X 
+		/*
+	 * ---------- change the translucent tint colour ----------
+	 */
+	if (has_translucent_tint_changed)
+	{
+		/* user specified colour */
+		if (translucent_tint != NULL)
+		{
+			PictureFreeColors(
+				dpy, Pcmap, &cs->translucent_tint, 1, 0, True);
+			cs->translucent_tint = GetColor(translucent_tint);
+		}
+		else
+		{
+			/* default */
+			PictureFreeColors(
+				dpy, Pcmap, &cs->translucent_tint, 1, 0, True);
+			cs->translucent_tint = GetColor(black);
+		}
+	}
+
X 	/*
X 	 * ---------- send new colorset to fvwm and clean up ----------
X 	 */
@@ -1700,6 +1747,7 @@
X 			ncs->fgsh = GetColor(white);
X 			ncs->tint = GetColor(black);
X 			ncs->icon_tint = GetColor(black);
+			ncs->translucent_tint = GetColor(black);
X 			ncs->pixmap = XCreatePixmapFromBitmapData(
X 				dpy, Scr.NoFocusWin,
X 				&g_bits[4 * (nColorsets % 3)], 4, 4,
@@ -1717,6 +1765,7 @@
X 			ncs->fgsh = GetForeShadow(ncs->fg, ncs->bg);
X 			ncs->tint = GetColor(black);
X 			ncs->icon_tint = GetColor(black);
+			ncs->translucent_tint = GetColor(black);
X 		}
X 		ncs->fg_tint = ncs->bg_tint = GetColor(black);
X 		/* set flags for fg contrast, bg average */
@@ -1728,6 +1777,7 @@
X 		ncs->icon_alpha_percent = 100;
X 		ncs->tint_percent = 0;
X 		ncs->icon_tint_percent = 0;
+		ncs->translucent_tint_percent = 0;
X 		ncs->fg_tint_percent = ncs->bg_tint_percent = 0;
X 		ncs->dither = (PictureDitherByDefault())? True:False;
X 		nColorsets++;
diff -ruN fvwm.orig/fvwm/menus.c fvwm/fvwm/menus.c
--- fvwm.orig/fvwm/menus.c	2004-08-25 07:00:34.294484872 +0100
+++ fvwm/fvwm/menus.c	2004-08-25 07:00:40.506540496 +0100
@@ -65,6 +65,11 @@
X 
X /* ---------------------------- local macros ------------------------------- */
X 
+#define MENU_IS_TRANSLUCENT(mr,cs) \
+        (!MR_IS_TEAR_OFF_MENU(mr) && CSET_IS_TRANSLUCENT(cs))
+#define MENU_IS_TRANSPARENT(mr,cs) \
+        (MENU_IS_TRANSLUCENT(mr,cs) || CSET_IS_TRANSPARENT(cs))
+				    
X /* ---------------------------- imports ------------------------------------ */
X 
X /* This external is safe. It's written only during startup. */
@@ -407,7 +412,7 @@
X 
X 		/* move it back */
X 		if (ST_HAS_MENU_CSET(MR_STYLE(mr)) &&
-		    CSET_IS_TRANSPARENT(ST_CSET_MENU(MR_STYLE(mr))))
+		    MENU_IS_TRANSPARENT(mr,ST_CSET_MENU(MR_STYLE(mr))))
X 		{
X 			transparent_bg = True;
X 			get_menu_repaint_transparent_parameters(
@@ -2430,6 +2435,7 @@
X 				/* Doh.  Use the standard display instead. */
X 				MR_CREATE_DPY(mr) = dpy;
X 			}
+			MR_IS_TEAR_OFF_MENU(mr) = 1;
X 		}
X 		else
X 		{
@@ -3213,7 +3219,38 @@
X 	}
X 	MR_IS_PAINTED(mr) = 1;
X 	/* paint the menu background */
-	if (ms && ST_HAS_MENU_CSET(ms))
+	if (ms && ST_HAS_MENU_CSET(ms) &&
+	    MENU_IS_TRANSLUCENT(mr,ST_CSET_MENU(ms)))
+	{
+		Pixmap trans = None;
+		FvwmRenderAttributes fra;
+		colorset_t *colorset = &Colorset[ST_CSET_MENU(ms)];
+	
+		fra.mask = 0;
+		if (colorset->translucent_tint_percent > 0)
+		{
+			fra.mask = FRAM_HAVE_TINT;
+			fra.tint = colorset->translucent_tint;
+			fra.tint_percent = colorset->translucent_tint_percent;
+		}
+		if (MR_IS_BACKGROUND_SET(mr) == False)
+		{
+			trans = PGraphicsCreateTranslucent(
+				dpy, MR_WINDOW(mr), &fra,
+				BACK_GC(ST_MENU_INACTIVE_GCS(ms)),
+				MR_X(mr), MR_Y(mr), MR_WIDTH(mr), MR_HEIGHT(mr));
+			XMapRaised(dpy, MR_WINDOW(mr));
+			if (trans != None)
+			{
+				XSetWindowBackgroundPixmap(
+					dpy, MR_WINDOW(mr), trans);
+				MR_IS_BACKGROUND_SET(mr) = True;
+				clear_expose_menu_area(MR_WINDOW(mr), pevent);
+				XFreePixmap(dpy, trans);
+			}
+		}
+	}
+	else if (ms && ST_HAS_MENU_CSET(ms))
X 	{
X 		if (MR_IS_BACKGROUND_SET(mr) == False)
X 		{
@@ -4007,8 +4044,8 @@
X 				}
X 				MR_XANIMATION(parent_menu) += end_x - prev_x;
X 				if (ST_HAS_MENU_CSET(MR_STYLE(parent_menu)) &&
-				    CSET_IS_TRANSPARENT(
-					    ST_CSET_MENU(MR_STYLE(mr))))
+				    MENU_IS_TRANSPARENT(
+					    mr,ST_CSET_MENU(MR_STYLE(mr))))
X 				{
X 					transparent_bg = True;
X 					get_menu_repaint_transparent_parameters(
@@ -4183,10 +4220,22 @@
X 	 */
X 
X 	XMoveWindow(dpy, MR_WINDOW(mr), x, y);
+	MR_X(mr) = x;
+	MR_Y(mr) = y;
X 	XSelectInput(dpy, MR_WINDOW(mr), event_mask);
-	XMapRaised(dpy, MR_WINDOW(mr));
-	if (popdown_window)
-		XUnmapWindow(dpy, popdown_window);
+	if (MR_STYLE(mr) && ST_HAS_MENU_CSET(MR_STYLE(mr)) &&
+	    MENU_IS_TRANSLUCENT(mr,ST_CSET_MENU(MR_STYLE(mr))))
+	{
+		if (popdown_window)
+			XUnmapWindow(dpy, popdown_window);
+		paint_menu(mr, NULL, fw);
+	}
+	else
+	{
+		XMapRaised(dpy, MR_WINDOW(mr));
+		if (popdown_window)
+			XUnmapWindow(dpy, popdown_window);
+	}
X 	XFlush(dpy);
X 	MR_MAPPED_COPIES(mr)++;
X 	MST_USAGE_COUNT(mr)++;
@@ -6634,15 +6683,45 @@
X 	{
X 		last = True;
X 	}
-	if (!last && CSET_IS_TRANSPARENT_PR_TINT(ST_CSET_MENU(ms)))
+	if (!last &&
+	    (CSET_IS_TRANSPARENT_PR_TINT(ST_CSET_MENU(ms)) ||
+	     MENU_IS_TRANSLUCENT(mr,ST_CSET_MENU(ms))))
X 	{
X 		/* too slow ... */
X 		return;
X 	}
-	SetWindowBackground(
-		dpy, MR_WINDOW(mr), MR_WIDTH(mr), MR_HEIGHT(mr),
-		&Colorset[ST_CSET_MENU(ms)], Pdepth,
-		FORE_GC(MST_MENU_INACTIVE_GCS(mr)), False);
+	if (MENU_IS_TRANSLUCENT(mr,ST_CSET_MENU(ms)))
+	{
+		Pixmap trans;
+		FvwmRenderAttributes fra;
+		colorset_t *colorset = &Colorset[ST_CSET_MENU(ms)];
+	
+		fra.mask = 0;
+		if (colorset->translucent_tint_percent > 0)
+		{
+			fra.mask = FRAM_HAVE_TINT;
+			fra.tint = colorset->translucent_tint;
+			fra.tint_percent = colorset->translucent_tint_percent;
+		}
+		XUnmapWindow(dpy, MR_WINDOW(mr));
+		MR_X(mr) = x;
+		MR_Y(mr) = y;
+		trans = PGraphicsCreateTranslucent(
+			dpy, MR_WINDOW(mr), &fra,
+			BACK_GC(ST_MENU_INACTIVE_GCS(ms)),
+			MR_X(mr), MR_Y(mr), MR_WIDTH(mr), MR_HEIGHT(mr));
+		XMapRaised(dpy, MR_WINDOW(mr));
+		XSetWindowBackgroundPixmap(
+			dpy, MR_WINDOW(mr), trans);
+		XFreePixmap(dpy, trans);
+	}
+	else
+	{
+		SetWindowBackground(
+			dpy, MR_WINDOW(mr), MR_WIDTH(mr), MR_HEIGHT(mr),
+			&Colorset[ST_CSET_MENU(ms)], Pdepth,
+			FORE_GC(MST_MENU_INACTIVE_GCS(mr)), False);
+	}
X 	/* redraw the background of non active item */
X 	for (mi = MR_FIRST_ITEM(mr); mi != NULL; mi = MI_NEXT_ITEM(mi))
X 	{
@@ -7274,10 +7353,12 @@
X 				SetWindowBackground(
X 					dpy, MR_WINDOW(mr), MR_WIDTH(mr),
X 					MR_HEIGHT(mr),
-					&Colorset[ST_CSET_MENU(ms)],
-					Pdepth,
+					&Colorset[ST_CSET_MENU(ms)], Pdepth,
X 					FORE_GC(MST_MENU_INACTIVE_GCS(mr)),
-					True);
+					False);
+				XClearArea(
+					dpy, MR_WINDOW(mr), 0, 0, MR_WIDTH(mr),
+					MR_HEIGHT(mr), True);
X 			}
X 			else if ((ST_HAS_ACTIVE_CSET(ms) &&
X 				  ST_CSET_ACTIVE(ms) == cset) ||
diff -ruN fvwm.orig/fvwm/menus.h fvwm/fvwm/menus.h
--- fvwm.orig/fvwm/menus.h	2004-08-25 07:00:34.295484720 +0100
+++ fvwm/fvwm/menus.h	2004-08-25 07:00:54.366433472 +0100
@@ -141,6 +141,9 @@
X 	MenuItem *submenu_item;
X 	/* x distance window was moved by animation */
X 	int xanimation;
+	/* x,y XMapRaise */
+	int x;
+	int y;
X 	/* dynamic temp flags */
X 	struct
X 	{
@@ -182,6 +185,8 @@
X #define MR_SELECTED_ITEM(m)         ((m)->d->selected_item)
X #define MR_SUBMENU_ITEM(m)          ((m)->d->submenu_item)
X #define MR_XANIMATION(m)            ((m)->d->xanimation)
+#define MR_X(m)                     ((m)->d->x)
+#define MR_Y(m)                     ((m)->d->y)
X #define MR_STORED_ITEM(m)           ((m)->d->stored_item)
X #define MR_STORED_PIXELS(m)         ((m)->d->stored_pixels)
X /* flags */
diff -ruN fvwm.orig/libs/Colorset.h fvwm/libs/Colorset.h
--- fvwm.orig/libs/Colorset.h	2004-08-25 07:00:34.311482288 +0100
+++ fvwm/libs/Colorset.h	2004-08-25 07:00:54.366433472 +0100
@@ -51,6 +51,10 @@
X 	Bool dither;
X 	Bool allows_buffered_transparency;
X 	Bool is_maybe_root_transparent;
+	/* only use by fvwm menu (non tear-off) */
+	Bool is_translucent;
+	Pixel translucent_tint;
+	unsigned int translucent_tint_percent : 7;
X #endif
X } colorset_t;
X 
@@ -78,6 +82,7 @@
X #define FG_TINT_SUPPLIED  0x100
X #define BG_TINT_SUPPLIED  0x200
X #define ICON_TINT_SUPPLIED 0x400
+#define TRANSLUCENT_TINT_SUPPLIED 0x800
X #endif
X 
X /* colorsets are stored as an array of structs to permit fast dereferencing */
@@ -153,6 +158,11 @@
X     (cset >= 0 && cset->pixmap == ParentRelative && \
X      cset->tint_percent > 0)
X 
+#define CSET_IS_TRANSLUCENT(cset) \
+    (cset >= 0 && Colorset[cset].is_translucent)
+#define CSETS_IS_TRANSLUCENT(cset) \
+    (cset && cset->is_translucent)
+
X #ifndef FVWM_COLORSET_PRIVATE
X /* Create n new colorsets, fvwm/colorset.c does its own thing (different size)
X  */
diff -ruN fvwm.orig/libs/PictureGraphics.c fvwm/libs/PictureGraphics.c
--- fvwm.orig/libs/PictureGraphics.c	2004-08-25 07:00:34.315481680 +0100
+++ fvwm/libs/PictureGraphics.c	2004-08-25 07:00:54.380431344 +0100
@@ -1338,7 +1338,7 @@
X 	}
X }
X 
-#if 0 /* humm... maybe usefull one day with menus */
+#if 1 /* humm... maybe usefull one day with menus */
X Pixmap PGraphicsCreateTranslucent(
X 	Display *dpy, Window win, FvwmRenderAttributes *fra, GC gc,
X 	int x, int y, int width, int height)
diff -ruN fvwm.orig/libs/PictureGraphics.h fvwm/libs/PictureGraphics.h
--- fvwm.orig/libs/PictureGraphics.h	2004-08-25 07:00:34.315481680 +0100
+++ fvwm/libs/PictureGraphics.h	2004-08-25 07:00:54.381431192 +0100
@@ -122,7 +122,9 @@
X 	Display *dpy, Window win, Pixel tint, int tint_percent,
X 	Drawable dest, Bool dest_is_a_window, GC gc, GC mono_gc, GC alpha_gc,
X 	int dest_x, int dest_y, int dest_w, int dest_h);
-
+Pixmap PGraphicsCreateTranslucent(
+	Display *dpy, Window win, FvwmRenderAttributes *fra, GC gc,
+	int x, int y, int width, int height);
X /* never used ! */
X Pixmap PGraphicsCreateDitherPixmap(
X 	Display *dpy, Window win, Drawable src, Pixmap mask, int depth, GC gc,
SHAR_EOF
  (set 20 08 05 15 21 45 21 'fvwm-translucency.diff'; eval "$shar_touch") &&
  chmod 0600 'fvwm-translucency.diff'
if test $? -ne 0
then ${echo} 'restore of fvwm-translucency.diff failed'
fi
  if ${md5check}
  then (
       ${MD5SUM} -c >/dev/null 2>&1 || ${echo} 'fvwm-translucency.diff: MD5 check failed'
       ) << SHAR_EOF
314d1fb9330744b83117e0d236b73887  fvwm-translucency.diff
SHAR_EOF
  else
test `LC_ALL=C wc -c < 'fvwm-translucency.diff'` -ne 11434 && \
  ${echo} 'restoration warning:  size of fvwm-translucency.diff is not 11434'
  fi
fi
if rm -fr ${lock_dir}
then ${echo} 'x - removed lock directory `'${lock_dir}\''.'
else ${echo} 'x - failed to remove lock directory `'${lock_dir}\''.'
  return 1
fi
return 0
}
